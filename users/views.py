from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from users.models import Payment, User

from .serializers import PaymentSerializer, UserSerializer


class UserCreateAPIView(CreateAPIView):
    """Контроллер для пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentListView(ListAPIView):
    """Контроллер для платежей"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["payment_course", "payment_lesson", "payment_method"]
    search_fields = ["payment_course", "payment_lesson", "payment_method"]
    ordering_fields = ["date_payment"]
    permission_classes = (IsAuthenticated,)
