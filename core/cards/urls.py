from . import views
from rest_framework.routers import DefaultRouter

app_name = 'cards'


router = DefaultRouter()
router.register(r'cards', views.CardViewSet, basename='cards')
urlpatterns = router.urls
