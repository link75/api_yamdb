from rest_framework import serializers
from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, Title, Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""
    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""
    class Meta:
        model = Genre
        fields = ("name", "slug")


class TitlePOSTSerializer(serializers.ModelSerializer):
    """Сериализатор для записи модели Serializer."""
    category = serializers.SlugRelatedField(
        slug_field="slug", many=False, queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug", many=True, queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = ("id", "name", "year", "description", "genre", "category")


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения модели Serializer."""
    category = CategorySerializer(many=False, required=False)
    genre = GenreSerializer(many=True, required=False)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
            "rating",
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    class Meta:
        fields = "__all__"
        model = Review
        read_only_fields = ("title",)

    def validate(self, data):
        title_id = self.context["view"].kwargs.get("title_id")
        author = self.context.get("request").user
        title = get_object_or_404(Title, id=title_id)
        if (
            title.reviews.filter(author=author).exists()
            and self.context.get("request").method != "PATCH"
        ):
            raise serializers.ValidationError(
                "Можно оставлять только один отзыв!"
            )
        return data

    def validate_score(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError("Недопустимое значение!")
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )

    class Meta:
        fields = "__all__"
        model = Comment
        read_only_fields = ("review",)
