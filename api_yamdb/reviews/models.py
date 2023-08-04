from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .constants import MAX_NAME_LENGTH, MAX_SLUG_LENGTH
from .validators import validate_year


class User(AbstractUser):

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    USER_ROLES = [
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin'),
    ]

    email = models.EmailField(
        'Email',
        max_length=254,
        unique=True
    )
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль',
        max_length=9,
        choices=USER_ROLES,
        default=USER,
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return self.username


class CategoryGenreBase(models.Model):
    name = models.CharField(
        max_length=MAX_NAME_LENGTH
    )
    slug = models.SlugField(
        max_length=MAX_SLUG_LENGTH,
        unique=True,
        verbose_name='slug'
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(CategoryGenreBase):
    """Описание модели категорий."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreBase):
    """Описание модели жанров."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Описание модели произведений."""

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name='Произведение'
    )
    year = models.PositiveIntegerField(
        verbose_name='Год выпуска',
        validators=(validate_year,)
    )
    description = models.TextField(
        max_length=512,
        verbose_name='Описание',
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр'
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
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class ReviewCommentBase(models.Model):
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        abstract = True
        ordering = ["-pub_date"]


class Review(ReviewCommentBase):
    """Описание модели жанров."""

    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
    )
    score = models.PositiveSmallIntegerField(
        verbose_name="Оценка",
        validators=[
            MinValueValidator(1, 'Оценка не может быть ниже 1'),
            MaxValueValidator(10, 'Оценка не может быть выше 10')
        ],
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_review"
            )
        ]

    def __str__(self):
        return f'{self.author} - {self.title}'


class Comment(ReviewCommentBase):
    """Описание модели комментариев."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self):
        return f'{self.author} - {self.review}'
