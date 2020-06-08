from django.contrib.auth.models import User, Group
from .models import SnippetModel, LANGUAGE_CHOICES, STYLE_CHOICES

from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']



class SnippetSerializer(serializers.ModelSerializer):
    """
    Stores a single snippet
    """

    class Meta:
        model = SnippetModel
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style']

    def create(self, validated_data):
        """
        Create and return a new `SnippetModel` instance, given the validated data.
        """
        return SnippetModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `SnippetModel` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance