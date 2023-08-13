from django.urls import path
from .views import LoginView, RegisterView

app_name = 'user'

urlpatterns = [
    path('login/', LoginView.as_view(), name='user_login'),
    path('register/', RegisterView.as_view(), name='user_register'),
]