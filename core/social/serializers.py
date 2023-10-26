from rest_framework import serializers

from social.models import SiteComment


class SiteCommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = SiteComment
        fields = ('id', 'user', 'username', 'message')
        read_only_fields = ('id', 'user',)

    def get_username(sefl, comment):
        return comment.user.username
