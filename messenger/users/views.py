from http import HTTPStatus

from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserPatchSerializer, UserSerializer


class UserAPIView(APIView):
    def get(self, request):
        data = UserSerializer(request.user).data
        return Response(data, status=HTTPStatus.OK)

    def patch(self, request):
        serializer = UserPatchSerializer(
            request.user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(status=HTTPStatus.OK)

        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
