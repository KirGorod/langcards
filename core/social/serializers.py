from rest_framework import serializers

from social.models import SiteComment


class SiteCommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = SiteComment
        fields = (
            'id', 'username', 'message', 'rating', 'created_at',
            'avatar'
        )
        read_only_fields = ('id', 'username', 'avatar', 'created_at',)

    def get_username(self, comment):
        return comment.user.username

    def get_avatar(self, comment):
        request = self.context.get('request')
        return request.build_absolute_uri(comment.user.avatar.url)
