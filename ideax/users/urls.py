from django.contrib.auth import views as auth_views
from django.urls import path

from .views import profile

urlpatterns = [
    path('accounts/login/', auth_views.login, name='login'),
    path('accounts/logout/', auth_views.logout, name='logout'),
    path('users/profile/', profile, name='profile'),
]
