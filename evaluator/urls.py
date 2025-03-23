from django.urls import path
from .views import home, run_code

urlpatterns = [
    path("", home, name="home"),
    path("evaluate/", run_code, name="run_code"),
]
