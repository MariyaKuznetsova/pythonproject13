from celery import shared_task
from django.core.mail import send_mail
from rest_framework.generics import get_object_or_404

from config.settings import EMAIL_HOST_USER
from study.models import Subscription, Course
from users.models import User


@shared_task
def send_information_about_subscription(user_id, course_id):
    """Отправка сообщения на почту об обновлении курса"""
    # user = get_object_or_404(User, pk=user_id)
    # course_item = get_object_or_404(Course, pk=course_id)
    # subs_item = Subscription.objects.filter(
    #     user_subscription=user, course_subscription=course_item
    # )
    # send_mail(
    #     subject="Обновление курса",
    #     message="Произошло обновление курса, вы можете ознакомится с новыми материалами.",
    #     from_email=EMAIL_HOST_USER,
    #     recipient_list=[subs_item.user_subscription.email,],
    # )
    print("Привет send_information_about_subscription!!!!!!!!!!!!!")


@shared_task
def add_numbers():
    print("Привет add_numbers!!!!!!!!!!!!!")







