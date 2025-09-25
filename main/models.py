from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary_storage.storage import MediaCloudinaryStorage
class Feedback(models.Model):
    name = models.CharField(max_length=155, null=False, verbose_name="Имя", help_text="Введите ваше имя",)
    email = models.EmailField(verbose_name="Электронная почта",help_text="Введите вашу почту")
    title = models.CharField(max_length=155, verbose_name="Тема",help_text="Введите тему сообщения")
    content = models.TextField(verbose_name="Содержание",help_text="Введите текст сообщения",)
    send_time = models.DateTimeField(auto_now_add=True, verbose_name="Время отправки",help_text="Время отправки сообщения")

class News(models.Model):
    CHOICE_TYPE = [
        ('News', 'Новости'),
        ('Events', 'События')
    ]

    title = models.CharField(max_length=300)
    content = models.TextField()
    image = models.ImageField(upload_to='news/', blank=True, null=True, storage=MediaCloudinaryStorage())
    sort = models.CharField(max_length=20, choices=CHOICE_TYPE, default='News')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CustomUser(AbstractUser):
    INSTITUTION_CHOICES = [
        ('MUIT', 'МУИТ'),
        ('KITE', 'КИТЭ'),
        ('COMTEHNO', 'КОМТЕХНО'),
    ]
    GRADUATE_STATUS_CHOICES = [
        ('employed', 'Устроился'),
        ('searching', 'Ищет работу'),
        ('not_interested', 'Незаинтересован'),
    ]


    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    institution = models.CharField(
        max_length=50,
        choices=INSTITUTION_CHOICES,
        verbose_name="Учебное заведение"
    )
    graduation_year = models.PositiveIntegerField()
    patronymic = models.CharField(max_length=150, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, storage=MediaCloudinaryStorage())
    is_graduate = models.BooleanField(default=False, verbose_name="Выпускник")
    graduate_status = models.CharField(
        max_length=20,
        choices=GRADUATE_STATUS_CHOICES,
        default='searching',
        verbose_name="Статус выпускника",
        help_text="Текущее состояние выпускника"
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "phone_number", "institution", "graduation_year"]

    def save(self, *args, **kwargs):
        if not self.username:
            base_username = f"{self.first_name}.{self.last_name}".lower()
            username = base_username
            counter = 1
            while CustomUser.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            self.username = username
        super().save(*args, **kwargs)