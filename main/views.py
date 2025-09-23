from django.shortcuts import render
from rest_framework import permissions, status, viewsets
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.tokens import RefreshToken
# main/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny


from .models import News, Feedback, CustomUser
from .serializers import (
    FeedBackSerializers, 
    NewsSerializers,
)

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Позволяет редактировать только админам, все остальные — только чтение
    """
    def has_permission(self, request, view):
        # read-only доступ для всех
        if view.action in ['list', 'retrieve']:
            return True
        # остальные действия только для админов
        return request.user and request.user.is_staff

class NewsListView(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializers
    permission_classes = [IsAdminOrReadOnly]

class FeedbackView(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedBackSerializers

    def get_permissions(self):
        # create доступ для всех, остальное только для админов
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
    

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

# main/views.py (продолжение)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # добавляем кастомные поля в токен
        token['email'] = user.email
        token['username'] = user.username
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer