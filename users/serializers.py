from rest_framework import serializers

from users.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор по платежам"""
    class Meta:
        model = Payment
        fields = "__all__"
