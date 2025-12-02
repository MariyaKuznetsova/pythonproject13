from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from users.models import Payment, User

from .serializers import PaymentSerializer, UserSerializer
from .services import create_stripe_price, create_stripe_session, create_stripe_product


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
        pay = serializer.save(user_payment=self.request.user)
        if pay.payment_course:
            name = pay.payment_course.name
            description = pay.payment_course.description
            product = create_stripe_product(name, description)
        elif pay.payment_lesson:
            name = pay.payment_lesson.name
            description = pay.payment_lesson.description
            product = create_stripe_product(name, description)
        price = create_stripe_price(product, pay.sum_payment)
        session_id, payment_link = create_stripe_session(price)
        pay.session_id = session_id
        pay.link = payment_link
        pay.save()
