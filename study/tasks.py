from datetime import timedelta, timezone

from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from users.models import User


@shared_task
def send_information_about_subscription(email):
    """Отправка письмо пользователю об уведомлении об обновлении курса"""
    send_mail(
        subject="Обновление курса",
        message="Произошло обновление курса, вы можете ознакомится с новыми материалами.",
        from_email=EMAIL_HOST_USER,
        recipient_list=[
            email,
        ],
    )


@shared_task
def deactivate_users():
    """Блокировка пользователя"""
    user = User.objects.all()
    for u in user:
        if timezone.now() - u.last_login > timedelta(days=30):
            u.is_active = False
            u.save()
