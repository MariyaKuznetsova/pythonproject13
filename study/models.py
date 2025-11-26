from django.conf import settings
from django.db import models


class Course(models.Model):
    """Класс курсы"""

    name = models.CharField(max_length=150, verbose_name="Название курса")
    description = models.CharField(max_length=150, verbose_name="Описание курса")
    image = models.ImageField(
        upload_to="images/", blank=True, null=True, verbose_name="Изображение"
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец курса",
        blank=True,
        null=True,
    )

    price = models.PositiveIntegerField(verbose_name='Цена курса', blank=True, null=True)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["name", "description", "price"]

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """Класс уроки"""

    name = models.CharField(max_length=150, verbose_name="Название урока")
    description = models.CharField(max_length=150, verbose_name="Описание урока")
    image = models.ImageField(
        upload_to="images/", blank=True, null=True, verbose_name="Изображение"
    )
    video = models.URLField(blank=True, null=True, verbose_name="Видео")
    courses = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Название курса",
        related_name="lessons",
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец урока",
        blank=True,
        null=True,
    )

    price = models.PositiveIntegerField(verbose_name='Цена урока', blank=True, null=True)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["name", "description", "courses", "price"]

    def __str__(self):
        return self.name


class Subscription(models.Model):
    """Класс подписки"""

    user_subscription = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )

    course_subscription = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ["user_subscription", "course_subscription"]

    def __str__(self):
        return self.user_subscription
