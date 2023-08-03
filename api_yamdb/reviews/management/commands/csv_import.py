import csv

from django.core.management import BaseCommand
from django.db import IntegrityError

from reviews.models import Category, Title, Genre, Comment, GenreTitle, Review
from users.models import User


TABLES = {
    Category: "category",
    Comment: "comments",
    GenreTitle: "genre_title",
    Genre: "genre",
    Review: "review",
    Title: "titles",
    User: "users",
}

FIELDS = {
    "category": ("category", Category),
    "genre_id": ("genre", Genre),
    "review_id": ("review", Review),
    "title_id": ("title", Title),
    "author": ("author", User),
}
