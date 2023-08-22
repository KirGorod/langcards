from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'cards'


router = DefaultRouter()
router.register(r'cards', views.CardViewSet, basename='cards')
urlpatterns = router.urls

urlpatterns += [
    path('learn/', views.LearnCardsView.as_view(), name='learn_cards'),
]
