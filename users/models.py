from django.contrib.auth.models import AbstractUser
from django.db import models

from study.models import Course, Lesson


class User(AbstractUser):
    """Модель пользователь"""
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Телефон")
    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True, verbose_name="Город")

    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)

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
    sum_payment = models.PositiveIntegerField()
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты")

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f'{self.users} - {self.data_payment}'

