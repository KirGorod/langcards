from . import views
from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = 'cards'


router = DefaultRouter()
router.register(r'cards', views.CardViewSet, basename='cards')
router.register(r'decks', views.DeckViewSet, basename='decks')
urlpatterns = router.urls

urlpatterns += [
    path(
        'learn/<int:deck_id>/',
        views.LearnCardsView.as_view(),
        name='learn_cards'
    ),
    path(
        'add_deck/<int:deck_id>/',
        views.AddDeckToLearningView.as_view(),
        name='add_learning_deck'
    ),

    # testing endpoints
    path('random_card/', views.RandomCardView.as_view(), name='random_card'),
]
