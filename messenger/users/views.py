from http import HTTPStatus

from rest_framework.response import Response
from rest_framework.views import APIView

from utils.centrifugo import (generate_connection_token,
                              generate_subscription_token)

from .serializers import UserPatchSerializer, UserSerializer


class UserAPIView(APIView):
    def get(self, request):
        data = UserSerializer(request.user).data
        data['con_token'] = generate_connection_token(
            request.user.id)
        data['sub_token'] = generate_subscription_token(
            request.user.id, request.user.id)
        return Response(data, status=HTTPStatus.OK)

    def patch(self, request):
        serializer = UserPatchSerializer(
            request.user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(status=HTTPStatus.OK)

        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
