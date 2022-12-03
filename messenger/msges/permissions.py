from rest_framework.permissions import BasePermission


class IsMessageOwner(BasePermission):
    def has_permission(self, request, view):
        msg_id = view.kwargs.get('msg_id')
        return request.user.messages.filter(id=msg_id).exists()
