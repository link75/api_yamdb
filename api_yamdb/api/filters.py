from django_filters import CharFilter, FilterSet
from reviews.models import Title


class TitleFilter(FilterSet):
    genre = CharFilter(
        field_name='genre__slug'
    )
    category = CharFilter(
        field_name='category__slug'
    )
    year = CharFilter(
        field_name='year'
    )
    name = CharFilter(
        field_name='name',
        lookup_expr='contains'
    )

    class Meta:
        model = Title
        fields = '__all__'
