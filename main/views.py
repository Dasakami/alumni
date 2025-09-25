from rest_framework import permissions, status, viewsets, generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import News, Feedback, CustomUser
from .serializers import (
    FeedBackSerializers, 
    NewsSerializers,
    RegisterSerializer,
    CustomUserSerializer,
    AdminUserSerializer
)

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        return request.user and request.user.is_staff

class NewsListView(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializers
    permission_classes = [IsAdminOrReadOnly]

class FeedbackView(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedBackSerializers

    def get_permissions(self):
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
    



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class GraduatesView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(is_graduate=True)
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]


class UserAdminViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email', 'phone_number']
    ordering_fields = ['graduation_year', 'is_graduate']
    def get_queryset(self):
        qs = super().get_queryset()
        is_graduate = self.request.query_params.get('is_graduate')
        if is_graduate is not None:
            if is_graduate.lower() in ['true', '1']:
                qs = qs.filter(is_graduate=True)
            elif is_graduate.lower() in ['false', '0']:
                qs = qs.filter(is_graduate=False)
        return qs
