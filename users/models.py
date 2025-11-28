from django.contrib.auth.models import AbstractUser
from django.db import models

from study.models import Course, Lesson


class User(AbstractUser):
    """Модель пользователь"""

    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Телефон"
    )
    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True, verbose_name="Город")

    token = models.CharField(
        max_length=100, verbose_name="Token", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    """Модель платежи"""

    user_payment = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Пользователь",
        related_name="user_payment",
    )
    date_payment = models.DateField(auto_now_add=True, verbose_name="Дата оплаты")
    payment_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Оплаченный курс",
        related_name="course_payment",
    )
    payment_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Оплаченный урок",
        related_name="lesson_payment",
    )
    sum_payment = models.PositiveIntegerField(verbose_name='Сумма платежа', blank=True, null=True)
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты"
    )

    session_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="Id сессии")
    link = models.URLField(max_length=500, blank=True, null=True, verbose_name="Ссылка на оплату")

    def save(self, *args, **kwargs):
        if self.payment_course:
            self.sum_payment = self.payment_course.price
        elif self.payment_lesson:
            self.sum_payment = self.payment_lesson.price

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"{self.user_payment}, {self.sum_payment}, {self.payment_lesson}, {self.payment_course} "


