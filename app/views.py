from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect, get_object_or_404

# from app.models import Post
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    View,
    CreateView,
    UpdateView,
    TemplateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView, LoginView
from django.views import View
from django.contrib import messages
from django.db.models import Count
from app.models import *
from app.forms import (
    RegistrationForm,
    UserRegisterForm,
    UserLoginForm
)

from django.contrib.auth.models import User

# *******************************************************************************************************
class HomeView(TemplateView):
    template_name = "app/home.html"


class AddMemberView(CreateView):
    template_name = "app/register.html"
    form_class = RegistrationForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Please pay first ")
            return render(request, template_name="app/payment.html")
        else:
            messages.error(request, "Cannot submit your data. ")
            return render(
                request,
                self.template_name,
                {"form": form},
            )


class UserRegisterView(View):
    template_name = "app/user_register.html"

    def get(self, request, *args, **kwargs):
        form = UserRegisterForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data["username"]).exists():
                return render(
                    request,
                    self.template_name,
                    {"form": form, "error_message": "Username already exists."},
                )
            elif User.objects.filter(email=form.cleaned_data["email"]).exists():
                return render(
                    request,
                    self.template_name,
                    {"form": form, "error_message": "Email already exists."},
                )
            elif form.cleaned_data["password"] != form.cleaned_data["password_repeat"]:
                return render(
                    request,
                    self.template_name,
                    {"form": form, "error_message": "Passwords do not match."},
                )
            else:
                user = User.objects.create_user(
                    form.cleaned_data["username"],
                    form.cleaned_data["email"],
                    form.cleaned_data["password"],
                )
                user.first_name = form.cleaned_data["first_name"]
                user.last_name = form.cleaned_data["last_name"]
                user.phone_number = form.cleaned_data["phone_number"]
                user.save()

                login(request, user)

                return redirect("user_login")

        return render(request, self.template_name, {"form": form})
    
    

class UserLoginView(View):
    template_name = "app/user_login.html"

    def get(self, request, *args, **kwargs):
        form = UserLoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                return render(
                    request,
                    self.template_name,
                    {"form": form, "error_message": "Invalid username or password."},
                )

        return render(request, self.template_name, {"form": form})   
    