from rest_framework.permissions import BasePermission


class IsChatMember(BasePermission):
    def has_permission(self, request, view):
        chat_id = view.kwargs.get('chat_id')
        return request.user.chats.filter(id=chat_id).exists()


class IsChatAdmin(BasePermission):
    def has_permission(self, request, view):
        chat_id = view.kwargs.get('chat_id')
        return request.user.admin.filter(id=chat_id).exists()
