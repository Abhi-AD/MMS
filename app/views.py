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
    CustomerProfileEditForm,
    UserLoginForm,
    CustomerRegistrationForm,
    CustomerApplyRequestForm,
)
from django.http import Http404
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError

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
                messages.success(
                    self.request,
                    f"Invalid username or password...!",
                )
                return render(
                    request,
                    self.template_name,
                    {"form": form},
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
            contact = form.cleaned_data["contact"]
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

                # Create related Customer instance
                Customer.objects.create(
                    member=user, contact=contact, images=images
                )
                messages.success(request, "Create a new account ...!")
                return super().form_valid(form)
            except Exception as e:
                # Handle any errors here
                # You can add error messages to the form or use a different approach to display errors
                messages.success(request, "An error occurred during registration.")
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)


# apply request
class SubmitApplicationView(LoginRequiredMixin, View):
    template_name = "app/register.html"
    form_class = CustomerApplyRequestForm
    login_url = "/user_login/"

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


# profile view
class UserProfileView(LoginRequiredMixin, View):
    template_name = "app/customer_profile.html"
    login_url = "/user_login/"

    def get(self, request, *args, **kwargs):
        try:
            # Assuming Customer model has a ForeignKey to the User model named 'member'
            user_profile = Customer.objects.get(member=request.user)
            context = {"user_profile": user_profile}
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            messages.success(request, "You are not Customer...!")
            return redirect("home")


# change password
class ChangePasswordView(LoginRequiredMixin, View):
    template_name = "app/customer_change_password.html"
    login_url = "/user_login/"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        error = ""
        user = request.user

        currentpassword = request.POST.get("currentpassword")
        newpassword = request.POST.get("newpassword")

        try:
            if user.check_password(currentpassword):
                user.set_password(newpassword)
                user.save()
                error = "no"
                messages.success(request, "Change Password Successfully")
                return redirect("user_login")
            else:
                error = "not"
        except Exception as e:
            print(e)
            error = "yes"

        return render(request, self.template_name, {"error": error})


# profil edit



class CustomerProfileEditView(LoginRequiredMixin, View):
    template_name = "app/customer_profile_edit.html"
    login_url = "/user_login/"

    def get(self, request, *args, **kwargs):
        try:
            customer = get_object_or_404(Customer, member=request.user)
            form = CustomerProfileEditForm(instance=customer)
            return render(
                request, self.template_name, {"form": form, "customer": customer}
            )
        except Http404:
            messages.error(request, "Customer not found.")
            return redirect("home")

    def post(self, request, *args, **kwargs):
        customer = get_object_or_404(Customer, member=request.user)
        form = CustomerProfileEditForm(request.POST, request.FILES, instance=customer)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")

        return render(request, self.template_name, {"form": form, "customer": customer})




# delete the account

class DeleteAccountView(LoginRequiredMixin,View):
    template_name = 'app/delete_account.html'
    login_url = "/user_login/"
    

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        messages.success(request, 'Your account has been deleted.')
        return redirect('home') 