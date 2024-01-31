from django.urls import path
from app import views
from app.views import *

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("register/", SubmitApplicationView.as_view(), name="register"),
    path("user_register/", RegistrationView.as_view(), name="user_register"),
    path("user_login/", UserLoginView.as_view(), name="user_login"),
    path("user_logout/", UserLogoutView.as_view(), name="user_logout"),
    path("profile/", CombinedProfileView.as_view(), name="profile"),
    path("change_password/", ChangePasswordView.as_view(), name="change_password"),
    path("profile_edit/", CustomerProfileEditView.as_view(), name="profile_edit"),
    path("delete_account/", DeleteAccountView.as_view(), name="delete_account"),
    path(
        "customer_service/<int:pk>/",
        CustomerServiceDetailView.as_view(),
        name="customer_service_view_detail",
    ),
    path(
        "service/<pk>/create_payment/",
        PaymentCreateView.as_view(),
        name="create_payment",
    ),
]
