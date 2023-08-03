from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Переопределение стандартной модели User."""
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

    USER_ROLES = [
        (USER, "User"),
        (MODERATOR, "Moderator"),
        (ADMIN, "Admin"),
    ]

    email = models.EmailField("email", max_length=254, unique=True)
    bio = models.TextField("Биография", blank=True)
    role = models.CharField(
        "Роль",
        max_length=9,
        choices=USER_ROLES,
        default=USER,
    )

    class Meta:
        ordering = ("username",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return self.username
