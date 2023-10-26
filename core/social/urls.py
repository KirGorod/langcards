from . import views
from rest_framework.routers import DefaultRouter

app_name = 'social'

router = DefaultRouter()
router.register(r'comments', views.SiteCommentViewSet, basename='comments')
urlpatterns = router.urls
