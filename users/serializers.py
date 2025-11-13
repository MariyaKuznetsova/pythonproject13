from rest_framework import serializers

from users.models import Payment, User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор по пользователям"""

    class Meta:
        model = User
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор по платежам"""

    class Meta:
        model = Payment
        fields = "__all__"
