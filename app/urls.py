from django.urls import path
from app import views
from app.views import *

urlpatterns = [
    #     path("", views.post_list, name='post-list'),
    path("", views.HomeView.as_view(), name="home"),
    path("register/", AddMemberView.as_view(), name="register"),
]
