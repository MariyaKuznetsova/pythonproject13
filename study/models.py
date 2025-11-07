from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название курса")
    description = models.CharField(max_length=150, verbose_name="Описание курса")
    image = models.ImageField(upload_to="images/", blank=True, null=True, verbose_name="Изображение")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["name", "description"]

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название урока")
    description = models.CharField(max_length=150, verbose_name="Описание урока")
    image = models.ImageField(upload_to="images/", blank=True, null=True, verbose_name="Изображение")
    video = models.URLField(blank=True, null=True, verbose_name="Видео")
    courses = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Название курса",
        related_name="lessons",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["name", "description", "courses"]

    def __str__(self):
        return self.name

