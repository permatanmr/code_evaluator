# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None  # Remove default username field
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email

from django.db import models

class Exam(models.Model):
    exam_name = models.CharField(max_length=255, unique=True)
    exam_code = models.CharField(max_length=50, unique=True)  # ✅ Unique exam code
    description = models.TextField()
    image = models.ImageField(upload_to='exam_images/', blank=True, null=True)
    duration_in_minutes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.exam_name} ({self.exam_code})"


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    ROLE_CHOICES = (
        ('python', 'python'),
        ('javascript', 'javascript'),
        ('dart', 'dart'),
    )
    programming_language = models.CharField(max_length=50, choices=ROLE_CHOICES)
    description = models.TextField()
    question_code = models.TextField()
    answer_code = models.TextField()
    expected_result = models.TextField()

    def __str__(self):
        return f"Question for {self.exam.exam_name}"
    