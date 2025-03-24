from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Exam, Question

admin.site.register(CustomUser)
admin.site.register(Exam)
admin.site.register(Question)

