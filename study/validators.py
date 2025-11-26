from rest_framework.serializers import ValidationError


def validate_forbidden_url(value):
    """Валидация ссылки на видео"""
    if not value.startswith("https://www.youtube.com"):
        return ValidationError("Неверная ссылка!")
