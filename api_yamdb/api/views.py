from django.conf import settings
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title, User
from .filters import TitleFilter
from .mixins import CreateDestroyListViewSet
from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsAuthorAdminModerOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, RegistrationSerializer,
                          ReviewSerializer, TitlePOSTSerializer,
                          TitleSerializer, TokenSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
            detail=False,
            methods=['get', 'patch'],
            permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)

        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data.get('role'):
            serializer.validated_data['role'] = request.user.role

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def signup(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')

    try:
        user, created = User.objects.get_or_create(
            username=username,
            email=email
        )
    except IntegrityError:
        raise ValidationError(
            'Данное имя пользователя (username) или email уже есть в базе!',
            status.HTTP_400_BAD_REQUEST
        )

    confirmation_code = default_token_generator.make_token(user)
    print(confirmation_code)

    send_mail(
        'Код подтверждения',
        f'{confirmation_code}',
        f'{settings.DEFAULT_EMAIL_TO_SEND_FROM}',
        [email],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def generate_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    confirmation_code = serializer.validated_data.get('confirmation_code')
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)

    if not default_token_generator.check_token(user, confirmation_code):
        return Response(
            data={'error': 'Неверный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    token = RefreshToken.for_user(user)

    return Response(
        data={
            'refresh': str(token),
            'access': str(token.access_token)
        },
        status=status.HTTP_200_OK
    )


class GenreViewSet(CreateDestroyListViewSet):
    """Вьюсет для получения жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для получения произведений."""

    queryset = Title.objects.annotate(rating=Avg('reviews__score')).order_by(
        'name'
    )
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitlePOSTSerializer
        return TitleSerializer


class CategoryViewSet(CreateDestroyListViewSet):
    """Вьюсет для получения категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для получения ревью."""

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorAdminModerOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для получения комментариев."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthorAdminModerOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
