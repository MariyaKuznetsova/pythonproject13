from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from users.models import Payment, User

from .serializers import PaymentSerializer, UserSerializer
from .services import create_stripe_price, create_stripe_products, create_stripe_session


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


class PaymentCreateAPIView(CreateAPIView):
    """Контроллер для оплаты"""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        product_payment = create_stripe_products(name=validated_data.get('name'), description=validated_data.get('description'))
        price = create_stripe_price(validated_data.get('sum_payment'))
        session_id, payment_link = create_stripe_session(price)
        payments = serializer.save(
            user=self.request.user,
            product_id=product_payment.id,
            price_id=price.id,
            session_id=validated_data.session_id,
            link=validated_data.payment_link
        )
        payments.save()

