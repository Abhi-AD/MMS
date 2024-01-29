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
    UserLoginForm,
    CustomerRegistrationForm,
    CustomerApplyRequestForm,
)
from django.views.generic.edit import FormView
from django.contrib.auth.models import User

# *******************************************************************************************************


# home view authications
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "app/home.html"
    login_url = "/user_login/"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# cutomer login
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
                messages.success(
                    self.request,
                    f"User LogIn Successfully {request.user.first_name} {request.user.last_name}...!",
                )
                return redirect("home")
            else:
                return render(
                    request,
                    self.template_name,
                    {"form": form, "error_message": "Invalid username or password."},
                )

        return render(request, self.template_name, {"form": form})


# cutomer logout
class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        first_name = request.user.first_name  # Get the username before logging out
        last_name = request.user.last_name  # Get the username before logging out
        logout(request)
        messages.success(
            request, f"User LogOut Successfully {first_name} {last_name}...!"
        )
        return redirect("home")


# customer register
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
                Customer.objects.create(
                    member=user, customercode=customercode, images=images
                )
                return super().form_valid(form)
            except Exception as e:
                # Handle any errors here
                # You can add error messages to the form or use a different approach to display errors
                form.add_error(None, "An error occurred during registration.")
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)


# apply request
class SubmitApplicationView(View):
    template_name = "app/register.html"
    form_class = CustomerApplyRequestForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            try:
                customer = Customer.objects.get(member=request.user)
            except Customer.DoesNotExist:
                messages.success(
                    request,
                    f"Customer Not Apply Request Successfully {request.user.username}...!,",
                )
            application = form.save(commit=False)
            application.member = customer
            messages.success(
                request,
                f"Customer Apply Request Successfully {request.user.username}...!,",
            )
            application.save()
            return redirect("register")  # Redirect to a success page
        else:
            # Print form errors to the console for debugging
            print(form.errors)

        return render(request, self.template_name, {"form": form})
