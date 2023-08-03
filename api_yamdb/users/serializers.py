from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role"
        )


class RegistrationSerializer(serializers.Serializer):
    """Сериализатор для регистрации."""
    username = serializers.CharField(
        max_length=150, validators=[UnicodeUsernameValidator()]
    )
    email = serializers.EmailField(max_length=254)

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError(
                'Пользователь не может быть "me"'
            )
        return value


class TokenSerializer(serializers.Serializer):
    """Сериализатор для токена аутентификации."""
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=254)
