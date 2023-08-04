import csv

from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title
from reviews.models import User

ThroughModel = Title.genre.through


class Command(BaseCommand):
    help = 'load data from csv'

    def handle(self, *args, **options):


        with open(
            'static/data/category.csv',
            encoding="utf-8-sig"
        ) as csv_file:

            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                id = row['id']
                name = row['name']
                slug = row['slug']
                category = Category(id=id, name=name, slug=slug)
                category.save()

        with open(
            'static/data/titles.csv',
            encoding="utf-8-sig"
        ) as csv_file:

            csv_reader = csv.DictReader(
                csv_file,
                delimiter=',',
                doublequote=False)
            for row in csv_reader:
                id = row['id']
                name = row['name']
                year = row['year']
                category_id = row['category']
                title = Title(id=id,
                              name=name,
                              year=year,
                              category=Category.objects.get(id=category_id))
                title.save()

        with open(
            'static/data/genre.csv',
            encoding="utf-8-sig"
        ) as csv_file:

            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                id = row['id']
                name = row['name']
                slug = row['slug']
                genre = Genre(id=id, name=name, slug=slug)
                genre.save()

        with open(
            'static/data/review.csv',
            encoding="utf-8-sig"
        ) as csv_file:

            csv_reader = csv.DictReader(csv_file, delimiter=',',)
            for row in csv_reader:
                id = row['id']
                title_id = row['title_id']
                text = row['text']
                author_id = row['author']
                author = User.objects.get(pk=author_id)
                score = row['score']
                pub_date = row['pub_date']
                review = Review(
                    id=id, title_id=title_id, text=text, author=author,
                    score=score, pub_date=pub_date
                )
                review.save()

        with open(
            'static/data/genre_title.csv',
            encoding="utf-8-sig"
        ) as csv_file:

            csv_reader = csv.DictReader(csv_file, delimiter=',',)
            for row in csv_reader:
                id = row['id']
                title_id = row['title_id']
                genre_id = row['genre_id']
                title_genre = ThroughModel(
                    id=id,
                    title=Title.objects.get(id=title_id),
                    genre=Genre.objects.get(id=genre_id)
                )
                title_genre.save()

        with open(
            'static/data/comments.csv',
            encoding="utf-8-sig"
        ) as csv_file:

            csv_reader = csv.DictReader(csv_file, delimiter=',',)
            for row in csv_reader:
                id = row['id']
                review_id = row['review_id']
                text = row['text']
                author_id = row['author']
                author = User.objects.get(pk=author_id)
                pub_date = row['pub_date']
                comment = Comment(
                    id=id,
                    review_id=review_id,
                    text=text,
                    author=author,
                    pub_date=pub_date
                )
                comment.save()

        with open(
            'static/data/users.csv',
            encoding="utf-8-sig"
        ) as csv_file:

            csv_reader = csv.DictReader(csv_file, delimiter=',',)
            for row in csv_reader:
                id = row['id']
                username = row['username']
                email = row['email']
                role = row['role']
                bio = row['bio']
                first_name = row['first_name']
                last_name = row['last_name']
                user = User(
                    id=id, username=username, email=email, role=role, bio=bio,
                    first_name=first_name, last_name=last_name
                )
                user.save()
