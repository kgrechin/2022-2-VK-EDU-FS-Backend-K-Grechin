from http import HTTPStatus

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from chats.models import Chat
from users.models import User

from .permissions import IsChatAdmin, IsChatMember
from .serializers import (ChatPatchSerializer, ChatPostSerializer,
                          ChatSerializer)
from .tasks import publish_chat, send_invitation


class ChatsAPIView(APIView):
    def get(self, request):
        queryset = request.user.chats.all()
        data = ChatSerializer(
            queryset, context={'request': request}, many=True).data
        return Response(data, status=HTTPStatus.OK)

    def post(self, request):
        request.data['members'].append(request.user.id)

        serializer = ChatPostSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()

            chat = Chat.objects.get(id=serializer.data['id'])
            members = User.objects.filter(id__in=serializer.data['members'])

            publish_data = ChatSerializer(
                chat, context={'request': request}).data

            for member in members:
                publish_chat.delay(publish_data, member.id)

                if member.email != chat.admin.email:
                    inviter = chat.admin.get_full_name()
                    send_invitation.delay(inviter, chat.title, [member.email])

            return Response({'id': chat.id}, status=HTTPStatus.OK)

        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


class ChatAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'PUT':
            permission_classes = [IsChatMember, IsChatAdmin]
        else:
            permission_classes = [IsChatMember]
        return [permission() for permission in permission_classes]

    def get(self, request, chat_id):
        queryset = Chat.objects.get(id=chat_id)
        return Response(ChatSerializer(queryset).data)

    def patch(self, request, chat_id):
        chat = Chat.objects.get(id=chat_id)

        serializer = ChatPatchSerializer(
            chat, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'complete'}, status=HTTPStatus.OK)

        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)

    def put(self, request, chat_id):
        user_id = request.data['user_id']

        user = get_object_or_404(User, id=user_id)
        chat = Chat.objects.get(id=chat_id)

        if chat.members.filter(id=user_id).exists():
            return Response({'detail': 'user already in chat'}, status=HTTPStatus.BAD_REQUEST)

        chat.members.add(user)
        return Response({'detail': 'complete'}, status=HTTPStatus.OK)
