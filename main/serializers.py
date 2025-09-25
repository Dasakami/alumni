from rest_framework import serializers
from .models import News, CustomUser, Feedback
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
class NewsSerializers(serializers.ModelSerializer):

    title = serializers.CharField(help_text="Заголовок новости")
    content = serializers.CharField(help_text="Содержимое новости")
    image = serializers.ImageField(help_text="Изображение новости", required=False)
    sort = serializers.CharField(help_text="Тип новости: News или Events")
    created_at = serializers.DateTimeField(help_text="Дата создания новости", read_only=True)
    updated_at = serializers.DateTimeField(help_text="Дата обновления новости", read_only=True)
    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'image', 'sort', 'created_at', 'updated_at' ]

        extra_kwargs = {
            'title': { 'example': 'Новость дня'},
            'content': { 'example': 'Содержание новости...'},
            'image': { 'example': '/media/news/example.jpg'},
        }

class FeedBackSerializers(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'name', 'email', 'title', 'content', 'send_time']





class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'patronymic', 'email', 'phone_number', 'institution', 'graduation_year', 'about', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            patronymic=validated_data.get('patronymic', ''),
            phone_number=validated_data['phone_number'],
            institution=validated_data['institution'],
            graduation_year=validated_data['graduation_year'],
            about=validated_data.get('about', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def to_representation(self, instance):
        """Возвращаем сразу JWT вместе с данными пользователя"""
        refresh = RefreshToken.for_user(instance)
        data = super().to_representation(instance)
        data['access'] = str(refresh.access_token)
        data['refresh'] = str(refresh)
        return data
    
class CustomUserSerializer(serializers.ModelSerializer):
    graduate_status = serializers.ChoiceField(
        choices=CustomUser.GRADUATE_STATUS_CHOICES,
        required=False,
        help_text="Статус выпускника (Устроился / Ищет работу / Незаинтересован)"
    )
    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'patronymic', 'phone_number', 'institution',
            'graduation_year', 'about', 'avatar', 'is_graduate', "graduate_status"
        ]
        read_only_fields = ['id', 'email', 'username', 'is_graduate']
    
class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'first_name', 'last_name', 'patronymic',
            'phone_number', 'institution', 'graduation_year', 'about',
            'avatar', 'is_graduate', 'graduate_status'
        ]
        read_only_fields = ['id', 'email', 'username'] 