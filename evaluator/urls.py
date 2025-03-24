from django.urls import path
from .views import run_code, register, login_view, logout_view, exam_take, exam_list, exam_detail

urlpatterns = [
    path("evaluate/", run_code, name="run_code"),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', exam_list, name='exam_list'),
    path('exams/<str:code>/', exam_detail, name='exam_detail'),
    path('take_exam/<str:code>', exam_take, name='take_exam'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)