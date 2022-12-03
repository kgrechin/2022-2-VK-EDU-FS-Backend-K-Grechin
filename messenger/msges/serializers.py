from rest_framework import serializers

from users.serializers import UserSerializer

from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Message
        fields = ('id', 'text', 'created_at', 'is_read', 'user', 'chat')


class MessagePostSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Message
        fields = ('id', 'text', 'user', 'chat')


class MessagePatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('text', )
