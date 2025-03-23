from django.urls import path
from .views import run_code, register, login_view, logout_view, exam_index

urlpatterns = [
    path("evaluate/", run_code, name="run_code"),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', exam_index, name='exam_index'),
]
