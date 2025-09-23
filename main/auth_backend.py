from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # ищем по email
            user = CustomUser.objects.get(email=username)
        except CustomUser.DoesNotExist:
            # если не нашли, пробуем по номеру
            try:
                user = CustomUser.objects.get(phone_number=username)
            except CustomUser.DoesNotExist:
                return None
        if user.check_password(password):
            return user
        return None