from http import HTTPStatus

from rest_framework.response import Response
from rest_framework.views import APIView

from chats.models import Chat
from chats.permissions import IsChatMember

from .models import Message
from .permissions import IsMessageOwner
from .serializers import (MessagePatchSerializer, MessagePostSerializer,
                          MessageSerializer)
from .tasks import publish_message
from .utils import parse_message_text


class MessagesAPIView(APIView):
    permission_classes = [IsChatMember]

    def get(self, request, chat_id):
        chat = Chat.objects.get(id=chat_id)
        data = MessageSerializer(chat.messages.all(), many=True).data
        return Response(data, status=HTTPStatus.OK)

    def post(self, request, chat_id):
        try:
            parse_message_text(request)
        except ValueError as error:
            return Response({'detail': str(error)}, status=HTTPStatus.BAD_REQUEST)

        request.data['chat'] = chat_id
        serializer = MessagePostSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()

            message = Message.objects.get(id=serializer.data['id'])
            publish_data = MessageSerializer(
                message, context={'request': request}).data

            publish_message.delay(publish_data, chat_id)
            return Response({'detail': 'complete'}, status=HTTPStatus.OK)

        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


class MessageAPIView(APIView):
    permission_classes = [IsMessageOwner]

    def get(self, request, msg_id):
        message = Message.objects.get(id=msg_id)
        return Response(MessageSerializer(message).data)

    def patch(self, request, msg_id):
        try:
            parse_message_text(request)
        except ValueError as error:
            return Response({'detail': str(error)}, status=HTTPStatus.BAD_REQUEST)

        message = Message.objects.get(id=msg_id)

        if message.is_read == True:
            request.data.pop('is_read')

        serializer = MessagePatchSerializer(
            message, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'complete'}, status=HTTPStatus.OK)

        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
