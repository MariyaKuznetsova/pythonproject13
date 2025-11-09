from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView

from users.models import Payment

from .serializers import PaymentSerializer


class PaymentListView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["payment_course", "payment_lesson", "payment_method"]
    search_fields = ["payment_course", "payment_lesson", "payment_method"]
    ordering_fields = ["date_payment"]
