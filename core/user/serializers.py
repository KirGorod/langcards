
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.db.models.functions import TruncDate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from cards.models import LearningLog
from core.fields import Base64ImageField

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
    avatar = Base64ImageField()
    progress = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password',  'first_name', 'last_name',
            'avatar', 'progress'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_progress(self, user):
        log_data = (
            LearningLog.objects.filter(user=user)
            .annotate(date=TruncDate('created_at'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )
        return {str(data['date']): data['count'] for data in log_data}

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        instance = super(UserSerializer, self).update(instance, validated_data)

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
