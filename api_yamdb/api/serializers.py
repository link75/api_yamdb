from rest_framework import serializers
from rest_framework.validators import ValidationError, UniqueTogetherValidator

from reviews.models import Genre, Review, Comment


class GenreSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(many=True,
                                         read_only=True,
                                         slug_field='genre')

    class Meta:
        model = Genre
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.PrimaryKeyRelatedField()
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = '__all__'

    validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title')
            )
        ]

    def validate(self, data):
        if data['text'] > 1:
            raise ValidationError(
                'Нельзя оставлять больше одного отзыва!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'