from django.core.management.base import BaseCommand

from users.models import Payment
from study.models import Course, Lesson


class Command(BaseCommand):
    help = "Add users to the database"

    def handle(self, *args, **kwargs):
        # Удаляем существующие записи
        Payment.objects.all().delete()

        payments = [
            {
                "user_payment": None,
                "payment_course": Course.objects.get(id=1),
                "payment_lesson": Lesson.objects.get(id=1),
                "sum_payment": 100000,
                "payment_method": "Наличные",
            },
            {
                "user_payment": None,
                "payment_course": Course.objects.get(id=1),
                "payment_lesson": Lesson.objects.get(id=1),
                "sum_payment": 50000,
                "payment_method": "Перевод на счет",
            },
        ]

        for payment_data in payments:
            payment, created = Payment.objects.get_or_create(**payment_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully added payment: {payment.user_payment}"))
            else:
                self.stdout.write(self.style.WARNING(f"Payment already exists: {payment.user_payment}"))
