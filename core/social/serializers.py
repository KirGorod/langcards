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
        user = comment.user
        username = user.username
        first_name = user.first_name
        last_name = user.last_name

        if first_name or last_name:
            return f'{first_name} {last_name}'.strip()
        return username

    def get_avatar(self, comment):
        request = self.context.get('request')
        if comment.user.avatar:
            return request.build_absolute_uri(comment.user.avatar.url)
        return None
