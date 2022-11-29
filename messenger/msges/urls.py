from django.urls import path

from .views import MessageAPIView, MessagesAPIView

urlpatterns = [
    path('messages/<uuid:chat_id>/', MessagesAPIView.as_view()),
    path('message/<uuid:msg_id>/', MessageAPIView.as_view())
]
