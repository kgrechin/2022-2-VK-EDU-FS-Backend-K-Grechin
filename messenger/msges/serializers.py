from rest_framework import serializers

from users.serializers import UserSerializer

from .models import Message, MessageImage


class MessageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageImage
        fields = ('id', 'image')


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        return MessageImageSerializer(obj.images.all(), many=True).data

    class Meta:
        model = Message
        fields = ('id', 'text', 'created_at',
                  'is_read', 'user', 'chat', 'images', 'voice')


class MessagePostSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Message
        fields = ('id', 'text', 'user', 'chat', 'voice')


class MessagePatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('text', )
