from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
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
        end_date = timezone.now()
        start_date = end_date - timedelta(weeks=3)
        dates_list = [
            (end_date - timedelta(days=x)).strftime('%Y-%m-%d')
            for x in range(0, (end_date - start_date).days + 1)
        ]

        log_data = (
            LearningLog.objects.filter(user=user)
            .annotate(date=TruncDate('created_at'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )

        progress = {str(data['date']): data['count'] for data in log_data}
        for date in dates_list:
            progress.setdefault(date, 0)

        return progress

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
