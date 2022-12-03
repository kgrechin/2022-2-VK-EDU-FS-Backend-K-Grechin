from django.urls import path

from .views import ChatAPIView, ChatsAPIView

urlpatterns = [
    path('chats/', ChatsAPIView.as_view()),
    path('chat/<uuid:chat_id>/', ChatAPIView.as_view())
]
