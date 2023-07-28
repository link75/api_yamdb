from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Role(models.Model):
    pass


class User(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE,
                             related_name='user')


# class Title(models.Model):
#     pass


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)
    # title = models.ForeignKey(
    #     Title, on_delete=models.CASCADE,
    #     related_name='genre'
    # )

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    # title = models.ForeignKey(
    #     Title, on_delete=models.CASCADE,
    #     related_name='genre'
    # )
    pud_date = models.DateField(
        'Дата публикации', auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'text'],
                name='unique_author_text'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pud_date = models.DateField(
        'Дата публикации', auto_now_add=True
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
    )

    def __str__(self):
        return '"{}" to review "{}" by author "{}"'.format(self.text,
                                                           self.review,
                                                           self.author)
