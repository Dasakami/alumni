from django.contrib import admin
from .models import News, Feedback, CustomUser
# Register your models here.

admin.site.register(News)
admin.site.register(Feedback)
admin.site.register(CustomUser)