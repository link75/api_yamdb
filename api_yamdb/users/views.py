from smtplib import SMTPResponseException

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from .models import User
from .permissions import IsAdmin
from .serializers import (RegistrationSerializer, TokenSerializer,
                          UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
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
def registration(request):
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
            'username or email already exists', status.HTTP_400_BAD_REQUEST
        )

    confirmation_code = default_token_generator.make_token(user)

    try:
        send_mail(
            'Confirmation code',
            f'{confirmation_code}',
            f'{settings.DEFAULT_EMAIL_TO_SEND_FROM}',
            [email],
            fail_silently=False,
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except SMTPResponseException:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def confirmation_code(request):
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
