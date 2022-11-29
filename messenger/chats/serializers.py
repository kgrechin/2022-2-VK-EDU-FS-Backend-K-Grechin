from rest_framework import serializers

from msges.serializers import MessageSerializer
from users.serializers import UserSerializer

from .models import Chat


class ChatSerializer(serializers.ModelSerializer):
    admin = UserSerializer()
    members = UserSerializer(many=True)

    last_message = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    def get_last_message(self, chat):
        return MessageSerializer(chat.messages.first()).data

    def get_title(self, chat):
        if chat.is_private:
            request = self.context.get('request')
            user = chat.members.all().exclude(id=request.user.id).first()
            return f'{user.first_name} {user.last_name}'
        return chat.title

    class Meta:
        model = Chat
        fields = ('id', 'title', 'avatar', 'is_private',
                  'created_at', 'admin', 'last_message', 'members')


class ChatPostSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    admin = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Chat
        fields = ('id', 'title', 'avatar', 'is_private', 'admin', 'members')


class ChatPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('title', 'avatar')
