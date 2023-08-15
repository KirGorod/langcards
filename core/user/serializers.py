from django.contrib.auth import get_user_model
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
    class Meta:
        model = User
        fields = (
            'username', 'email', 'password',
            'first_name', 'last_name'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super(UserSerializer, self).update(instance, validated_data)

        if password:
            instance.set_password(password)
            instance.save()

        return instance
