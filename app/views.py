from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm

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
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView, LoginView
from django.views import View
from django.contrib import messages
from django.db.models import Count
from app.models import *
from app.forms import (
    RegistrationForm,
    UserRegisterForm,
    UserLoginForm,
    CustomerRegistrationForm,
)
from django.views.generic.edit import FormView
from django.contrib.auth.models import User

# *******************************************************************************************************


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "app/home.html"
    login_url = "/user_login/"


class FormRegister(LoginRequiredMixin, CreateView):
    template_name = "app/register.html"
    form_class = RegistrationForm
    login_url = "/user_login/"

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


class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("home")




class RegistrationView(FormView):
    template_name = "app/user_register.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("user_login")  # Replace with the actual login URL

    def form_valid(self, form):
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            # Get data from the form
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            customercode = form.cleaned_data["customercode"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            images = form.cleaned_data["images"]

            try:
                # Create a new user
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                )

                # Create related EmployeeDetail instance
                Customer.objects.create(member=user, customercode=customercode, images=images)
                return super().form_valid(form)
            except Exception as e:
                # Handle any errors here
                # You can add error messages to the form or use a different approach to display errors
                form.add_error(None, "An error occurred during registration.")
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)





