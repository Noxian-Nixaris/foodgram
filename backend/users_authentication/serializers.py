import base64

from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer as BaseUserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers


User = get_user_model()


class AvatarSerializer(BaseUserSerializer):
    avatar = Base64ImageField(required=False, allow_null=True)

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('avatar',)

    def validate(self, data):
        avatar = data.get('avatar')
        if avatar is None:
            raise serializers.ValidationError()
        return data
