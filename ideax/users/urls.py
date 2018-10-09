from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('accounts/login/', auth_views.login, name='login'),
    path('accounts/logout/', auth_views.logout, name='logout'),
]
