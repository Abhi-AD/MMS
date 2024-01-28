from django.urls import path
from app import views
from app.views import *

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("register/", FormRegister.as_view(), name="register"),
    path("user_register/", RegistrationView.as_view(), name="user_register"),
    path("user_login/", UserLoginView.as_view(), name="user_login"),
    path("user_logout/", UserLogoutView.as_view(), name="user_logout"),
]
