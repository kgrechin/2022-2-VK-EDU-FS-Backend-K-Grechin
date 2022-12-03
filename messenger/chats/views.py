from http import HTTPStatus

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from chats.models import Chat
from users.models import User

from .permissions import IsChatMember
from .serializers import (ChatPatchSerializer, ChatPostSerializer,
                          ChatSerializer)
from .tasks import publish_chat, send_invitation


class ChatsAPIView(APIView):
    def get(self, request):
        queryset = request.user.chats.all()
        data = ChatSerializer(queryset, many=True, context={
                              'request': request}).data
        return Response(data, status=HTTPStatus.OK)

    def post(self, request):
        request.data['members'].append(request.user.id)

        serializer = ChatPostSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            chat = Chat.objects.get(id=serializer.data['id'])

            for member in serializer.data['members']:
                data = ChatSerializer(chat, context={'request': request}).data

                publish_chat.delay(data, member)

                member_email = User.objects.get(id=member).email

                if member_email != request.user.email:
                    send_invitation.delay(
                        request.user.get_full_name(), chat.title, [member_email])

            return Response(status=HTTPStatus.OK)

        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


class ChatAPIView(APIView):
    permission_classes = [IsChatMember]

    def get(self, request, chat_id):
        queryset = Chat.objects.get(id=chat_id)
        return Response(ChatSerializer(queryset).data)

    def patch(self, request, chat_id):
        chat = Chat.objects.get(id=chat_id)

        serializer = ChatPatchSerializer(
            chat, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(status=HTTPStatus.OK)

        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)

    def put(self, request, chat_id):
        user_id = request.data['user_id']

        user = get_object_or_404(User, id=user_id)
        chat = Chat.objects.get(id=chat_id)

        if chat.members.filter(id=user_id).exists():
            return Response({'detail': 'user already in chat'}, status=HTTPStatus.BAD_REQUEST)

        chat.members.add(user)
        return Response(status=HTTPStatus.OK)
