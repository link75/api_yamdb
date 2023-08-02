from django.db import models


class Category(models.Model):
    """Описание модели категорий."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        max_length=64,
        unique=True,
        verbose_name='slug',
    )

    class Meta:
        verbose_name = 'Категория'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Описание модели жанров."""

    name = models.CharField(
        max_length=128,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        max_length=64,
        verbose_name='slug',
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Описание модели произведений."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения'
    )
    year = models.PositiveIntegerField(
        verbose_name='Год выпуска',
    )
    description = models.TextField(
        max_length=512,
        verbose_name='Описание',
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
        verbose_name='Категория',

    )

    class Meta:
        verbose_name = 'Произведение'

    def __str__(self):
        return self.name
