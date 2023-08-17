import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    user_token = None
    avatar_base64 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password',  'first_name', 'last_name',
            'avatar', 'avatar_base64',
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        avatar_base64 = validated_data.get('avatar_base64')
        instance = super(UserSerializer, self).update(instance, validated_data)

        if avatar_base64:
            format, imgstr = avatar_base64.split(';base64,')
            ext = format.split('/')[-1]
            avatar_file = ContentFile(
                base64.b64decode(imgstr),
                name='avatar.' + ext
            )
            instance.avatar = avatar_file

        if password:
            instance.set_password(password)
            Token.objects.filter(user=instance).delete()
            token = Token.objects.create(user=instance)
            self.user_token = token.key

        instance.save()
        return instance

    def to_representation(self, instance):
        context = super().to_representation(instance)

        if self.user_token:
            context['token'] = self.user_token

        return context
