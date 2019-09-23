from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.user.authorisation.validators import TokenValidator


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password", "groups")


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("url", "name")


class TokenSerializer(serializers.Serializer):

    def __init__(self, *, user, **kwargs):
        super().__init__(**kwargs)
        self.user = user

    token = serializers.SlugField(max_length=255)

    def validate_token(self, value):
        token_val = TokenValidator(self.user)
        token_val(value)
        return value
