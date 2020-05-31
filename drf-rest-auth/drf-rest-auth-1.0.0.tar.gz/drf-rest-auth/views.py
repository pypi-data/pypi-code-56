"""
# Copyright © Nico Huebschmann
# Licensed under the terms of the MIT License
"""

from django.core.exceptions import ImproperlyConfigured
from django.contrib import auth as django_auth
from django.utils.translation import ugettext_lazy as _

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .utils import jwt
from .serializer import EmptySerializer, LoginSerializer, UserTokenSerializer, PasswordChangeSerializer, \
    PasswordResetSerializer, PasswordResetConfirmSerializer


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = EmptySerializer
    serializer_classes = {
        'login': LoginSerializer,
        'password_change': PasswordChangeSerializer,
        'password_reset': PasswordResetSerializer,
        'password_reset_confirm': PasswordResetConfirmSerializer,
    }

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured('serializer_classes should be a dict mapping.')

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        django_auth.login(self.request, user)
        data = {
            'user': user,
            'token': jwt.get_token_for_user(user)
        }
        return Response(
            data=UserTokenSerializer(instance=data, context={'request': request}).data,
            status=status.HTTP_200_OK
        )

    @action(methods=['POST', ], detail=False, permission_classes=[IsAuthenticated, ])
    def logout(self, request):
        django_auth.logout(request)
        return Response(
            data={'success': _('Successfully logged out.')},
            status=status.HTTP_200_OK
        )

    @action(url_path='password-change', methods=['POST'], detail=False, permission_classes=[IsAuthenticated, ])
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(
            data={'success': _('New password has been set.')},
            status=status.HTTP_200_OK
        )

    @action(url_path='password-reset', methods=['POST'], detail=False)
    def password_reset(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(reset_confirm_url=self.reverse_action(self.password_reset_confirm.url_name))
        return Response(
            data={'success': _('Password reset e-mail has been sent.')},
            status=status.HTTP_200_OK
        )

    @action(url_path='password-reset-confirm', methods=['POST'], detail=False)
    def password_reset_confirm(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={'success': _('Password has been reset.')},
            status=status.HTTP_200_OK
        )
