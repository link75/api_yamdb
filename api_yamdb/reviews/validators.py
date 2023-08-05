import re

from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(
            f'Год выпуска {value} не может быть больше {current_year}!'
        )


def validate_username(value):
    invalid_usernames = ['me']

    if value.lower() in invalid_usernames:
        raise ValidationError(f"Имя пользователя не может быть '{value}'!")

    valid_username_pattern = re.compile(r'[\w.@+-]+')
    bad_characters_in_username = list(
        filter(None, valid_username_pattern.split(value))
    )

    if bad_characters_in_username:
        raise ValidationError(
            f'Недопустимые символы {bad_characters_in_username} '
            f'в имени пользователя {value}!'
        )
