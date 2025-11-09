from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import PaymentListView

app_name = UsersConfig.name


urlpatterns = [
    path("payment/", PaymentListView.as_view(), name="payment_list"),
]
