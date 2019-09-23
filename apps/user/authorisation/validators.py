from rest_framework import serializers

from apps.user.authorisation.tokens import account_activation_token


class TokenValidator:
    def __init__(self, user):
        self.user = user

    def __call__(self, value):
        if not account_activation_token.check_token(self.user, value):
            message = 'Token is not valid.'
            raise serializers.ValidationError(message)
