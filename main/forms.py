from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "first_name", "last_name",
                  "phone_number", "institution", "graduation_year")

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name",
                  "phone_number", "institution", "graduation_year",
                  "is_active", "is_staff", "is_superuser", "groups", "user_permissions")
