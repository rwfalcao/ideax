from django.contrib.auth import views as auth_views
from django.urls import path
from .views import administration

urlpatterns = [
    path('', administration, name='index'),
]
