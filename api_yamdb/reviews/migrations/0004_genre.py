# Generated by Django 3.2 on 2023-07-31 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_delete_genre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
    ]
