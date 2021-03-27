from django.urls import path

from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('users', views.users_list, name='main'),
    path('refreshToken', views.refresh_token, name='tokenRefresh')
]