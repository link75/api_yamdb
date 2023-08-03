from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User


class Category(models.Model):
    """Описание модели категорий."""

    name = models.CharField(
        max_length=256,
        verbose_name="Название категории",
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="slug",
    )

    class Meta:
        verbose_name = "Категория"
        ordering = ("name",)


class Genre(models.Model):
    """Описание модели жанров."""

    name = models.CharField(max_length=128, verbose_name="Название жанра")
    slug = models.SlugField(
        max_length=50,
        verbose_name="slug",
        unique=True,
    )

    class Meta:
        verbose_name = "Жанр"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Описание модели произведений."""

    name = models.CharField(
        max_length=256,
        verbose_name="Название произведения"
    )
    year = models.PositiveIntegerField(
        verbose_name="Год выпуска",
    )
    description = models.TextField(
        max_length=512,
        verbose_name="Описание",
        blank=True,
    )
    genre = models.ManyToManyField(Genre, through="GenreTitle")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="titles",
        verbose_name="Категория",
    )

    class Meta:
        verbose_name = "Произведение"

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель, связывающая Genre и Title."""
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.genre}"


class Role(models.Model):
    pass


class Review(models.Model):
    """Описание модели жанров."""

    title = models.ForeignKey(
        Title,
        verbose_name="Произведение",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    text = models.TextField(
        verbose_name="Текст",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор",
    )
    score = models.SmallIntegerField(
        verbose_name="Оценка",
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-pub_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"],
                name="unique_review"
            )
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    """Описание модели комментариев."""

    text = models.TextField(
        verbose_name="Текст",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Пользователь",
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации", auto_now_add=True, db_index=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв",
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text
