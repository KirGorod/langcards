from django.urls import path
from .views import LoginView, RegisterView, UserProfileView

app_name = 'user'

urlpatterns = [
    path('login/', LoginView.as_view(), name='user_login'),
    path('register/', RegisterView.as_view(), name='user_register'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]
