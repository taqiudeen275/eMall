from django.urls import path
from .views import *

app_name = "account"
urlpatterns = [
    path('login', loginView, name='login'),
    path('register', signupView, name='register'),
    path('logout', logoutView, name='logout'),
]