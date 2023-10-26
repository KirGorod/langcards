from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated

from social.models import SiteComment
from social.serializers import SiteCommentSerializer


class SiteCommentViewSet(viewsets.ModelViewSet):
    renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]

    model = SiteComment
    serializer_class = SiteCommentSerializer

    def get_object(self):
        obj_id = self.kwargs.get('pk')
        user = self.request.user
        return get_object_or_404(SiteComment, id=obj_id, user=user)

    def get_queryset(self):
        return SiteComment.objects.all()[:10]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
