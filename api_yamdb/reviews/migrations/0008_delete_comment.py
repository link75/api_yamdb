# Generated by Django 3.2 on 2023-07-27 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_alter_comment_review'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
