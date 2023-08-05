from django.contrib import admin

from .models import User, Title, Comment, Review, Genre, Category


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'role',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
    )
    empty_value_display = 'пустое значение'
    list_editable = ('role',)
    list_filter = ('role',)
    search_fields = ('pk', 'username', 'role', 'email',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'category'
    )
    search_fields = ('name',)
    empty_value_display = 'пустое значение'
    list_filter = ('category',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    search_fields = ('name', 'pk', 'slug')
    empty_value_display = 'пустое значение'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    empty_value_display = 'пустое значение'
    search_fields = ('name',)


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'text',
        'pub_date',
        'review'
    )
    list_filter = ('author',)
    empty_value_display = 'пустое значение'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'title',
        'text',
        'score'
    )
    search_fields = ('text',)
    list_filter = ('author',)
    empty_value_display = 'пустое значение'
