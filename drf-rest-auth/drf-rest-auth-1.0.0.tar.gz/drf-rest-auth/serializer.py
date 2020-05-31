"""
# Copyright © Nico Huebschmann
# Licensed under the terms of the MIT License
"""

from importlib import import_module

from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator

from rest_framework import serializers

from .utils.forms import PasswordResetForm


class EmptySerializer(serializers.Serializer):
    pass


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(self.context['request'], username=username, password=password)
        if not user:
            raise serializers.ValidationError(_('Authentication failed with provided credentials.'))

        if not user.is_active:
            raise serializers.ValidationError(_('User account has been disabled.'))

        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']


class UserTokenSerializer(serializers.Serializer):
    token = serializers.CharField()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        """ Allows the use of a custom USER_SERIALIZER."""

        serializer_class = getattr(settings, 'REST_AUTH_USER_SERIALIZER', UserSerializer)
        if not hasattr(serializer_class, '__call__'):
            assert isinstance(serializer_class, str)
            module, class_name = serializer_class.rsplit('.', 1)
            serializer_class = getattr(import_module(module), class_name)
        return serializer_class(obj['user'], context=self.context).data


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, style={'input_type': 'password'})
    new_password = serializers.CharField(required=True, style={'input_type': 'password'})

    def validate_old_password(self, password):
        if not self.context['request'].user.check_password(password):
            raise serializers.ValidationError(_('Current password does not match.'))
        return password

    def validate_new_password(self, password):
        validate_password(password)
        return password


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)

    password_reset_form = None

    def validate_email(self, email):
        self.password_reset_form = PasswordResetForm(data=self.initial_data)
        if not self.password_reset_form.is_valid():
            raise serializers.ValidationError(self.password_reset_form.errors)
        return email

    def save(self, **kwargs):
        request = self.context.get('request')
        options = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
            'extra_email_context': {'reset_confirm_url': kwargs.get('reset_confirm_url')}
        }
        self.password_reset_form.save(**options)


class PasswordResetConfirmSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True, max_length=128, style={'input_type': 'password'})
    new_password2 = serializers.CharField(required=True, max_length=128, style={'input_type': 'password'})

    set_password_form = None

    def validate(self, attributes):
        try:
            user = get_user_model().objects.get(username=attributes.get('username'))
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError({'username': _('User does not exist.')})

        if not default_token_generator.check_token(user, attributes['token']):
            raise serializers.ValidationError({'token': _('Incorrect token.')})

        self.set_password_form = SetPasswordForm(user=user, data=attributes)
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attributes

    def save(self):
        return self.set_password_form.save()
