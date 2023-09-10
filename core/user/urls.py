from django.urls import path
from .views import LoginView, RegisterView, UserProfileView, GoogleAuthView
app_name = 'user'

urlpatterns = [
    path('login/', LoginView.as_view(), name='user_login'),
    path('google_auth/', GoogleAuthView.as_view(), name='google_auth'),
    path('register/', RegisterView.as_view(), name='user_register'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]
