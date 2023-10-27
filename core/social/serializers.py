from rest_framework import serializers

from social.models import SiteComment


class SiteCommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = SiteComment
        fields = ('id', 'username', 'message', 'rating', 'created_at')
        read_only_fields = ('id', 'username', 'created_at',)

    def get_username(sefl, comment):
        return comment.user.username
