from django.core.mail import send_mail

from application.settings import EMAIL_HOST_USER


def send_chat_add_notification(inviter, chat, recipients):
    send_mail(
        subject='Вас добавили в новый чат',
        message=f'{inviter} добавил вас в чат {chat}',
        from_email=EMAIL_HOST_USER,
        recipient_list=recipients
    )
