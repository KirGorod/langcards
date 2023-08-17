import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers

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
    password_old = serializers.CharField(write_only=True)
    password_new = serializers.CharField(write_only=True)
    avatar_base64 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password_old', 'password_new', 'first_name',
            'last_name', 'avatar', 'avatar_base64',
        )

    def validate_password_old(self, password_old):
        user = self.instance
        if not user.check_password(password_old):
            raise serializers.ValidationError('Wrong old password')
        return password_old

    def update(self, instance, validated_data):
        password_old = validated_data.get('password_old')
        password_new = validated_data.get('password_new')
        avatar_base64 = validated_data.get('avatar_base64')
        user = super(UserSerializer, self).update(instance, validated_data)

        if password_old and password_new:
            user.set_password(password_new)

        if avatar_base64:
            format, imgstr = avatar_base64.split(';base64,')
            ext = format.split('/')[-1]
            avatar_file = ContentFile(
                base64.b64decode(imgstr),
                name='avatar.' + ext
            )
            user.avatar = avatar_file

        user.save()
        return user
