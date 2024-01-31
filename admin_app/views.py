# django libaries
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, CreateView, DetailView, DeleteView,UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.views import PasswordChangeView

# cutom import
from admin_app.models import *
from app.models import *
from app.models import *
from admin_app.forms import (
    PaymentForm,
    RequestRegistrationForm,
    ServiceForm,
    SuperuserCreationForm,
)


# create the view
class MainView(View):
    template_name = "main/super_user_login.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")

        # authenticate
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            # Only allow superusers to log in
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect("main")
        else:
            messages.error(request, "Username or Password is incorrect.")
            return redirect("main")


# all payment history
class PaymentListView(ListView):
    model = ServicePayment
    template_name = "main/payment/payment_list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = ServicePayment.objects.all().order_by("-payment_date")
        for i, obj in enumerate(queryset, start=1):
            obj.serial_number = i
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Calculate total amount
        total_amount = ServicePayment.objects.aggregate(total_amount=models.Sum("amount"))[
            "total_amount"
        ]

        # Add total_amount to the context
        context["total_amount"] = total_amount

        return context


# payment create
class PaymentCreateView(CreateView):
    template_name = "main/payment/payment_form.html"
    form_class = PaymentForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Successfully submitted your query. We will transaction you soon ",
            )
            return redirect("payment_history")
        else:
            messages.error(request, "Cannot submit your data. ")
            return render(
                request,
                self.template_name,
                {"form": form},
            )


# admin logout
class AdminLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("main")


# cutomer request list
class CustomerFormListView(ListView):
    model = CustomerApplyRequest
    template_name = "main/All request/apply_list.html"
    context_object_name = "obj"  # Variable name used in the template
    queryset = CustomerApplyRequest.objects.all().order_by("-update_at")
    paginate_by = 10  # Number of items to display per page

    def get_queryset(self):
        queryset = super().get_queryset()
        for i, obj in enumerate(queryset, start=1):
            obj.serial_number = i
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_request_count = CustomerApplyRequest.objects.all().count()
        pending_count = PendingCustomerRequest.objects.all().count()
        pending_approval_count = PendingApprovalModel.objects.all().count()
        approved_count = ApprovedCustomerRequest.objects.all().count()
        rejected_count = RejectedCustomerRequest.objects.all().count()

        # Add counts to the context
        context["total_request_count"] = total_request_count
        context["pending_count"] = pending_count
        context["pending_approval_count"] = pending_approval_count
        context["approved_count"] = approved_count
        context["rejected_count"] = rejected_count

        return context


# cutomer pending request list
class CustomerPendingFormListView(ListView):
    model = PendingCustomerRequest
    template_name = "main/All request/apply_list pending.html"
    context_object_name = "obj"  # Variable name used in the template
    queryset = PendingCustomerRequest.objects.all().order_by("-update_at")
    paginate_by = 10  # Number of items to display per page

    def get_queryset(self):
        queryset = super().get_queryset()
        for i, obj in enumerate(queryset, start=1):
            obj.serial_number = i
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_request_count = CustomerApplyRequest.objects.all().count()
        pending_count = PendingCustomerRequest.objects.all().count()
        pending_approval_count = PendingApprovalModel.objects.all().count()
        approved_count = ApprovedCustomerRequest.objects.all().count()
        rejected_count = RejectedCustomerRequest.objects.all().count()

        # Add counts to the context
        context["total_request_count"] = total_request_count
        context["pending_count"] = pending_count
        context["pending_approval_count"] = pending_approval_count
        context["approved_count"] = approved_count
        context["rejected_count"] = rejected_count

        return context


# cutomer pending approval request list
class CustomerPendingApprovalFormListView(ListView):
    model = PendingApprovalModel
    template_name = "main/All request/apply_list pending approval.html"
    context_object_name = "obj"  # Variable name used in the template
    queryset = PendingApprovalModel.objects.all().order_by("-update_at")
    paginate_by = 10  # Number of items to display per page

    def get_queryset(self):
        queryset = super().get_queryset()
        for i, obj in enumerate(queryset, start=1):
            obj.serial_number = i
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_request_count = CustomerApplyRequest.objects.all().count()
        pending_count = PendingCustomerRequest.objects.all().count()
        pending_approval_count = PendingApprovalModel.objects.all().count()
        approved_count = ApprovedCustomerRequest.objects.all().count()
        rejected_count = RejectedCustomerRequest.objects.all().count()

        # Add counts to the context
        context["total_request_count"] = total_request_count
        context["pending_count"] = pending_count
        context["pending_approval_count"] = pending_approval_count
        context["approved_count"] = approved_count
        context["rejected_count"] = rejected_count

        return context


# cutomer apropval request list
class CustomerApprovalFormListView(ListView):
    model = ApprovedCustomerRequest
    template_name = "main/All request/apply_list approval.html"
    context_object_name = "obj"  # Variable name used in the template
    queryset = ApprovedCustomerRequest.objects.all().order_by("-update_at")
    paginate_by = 10  # Number of items to display per page

    def get_queryset(self):
        queryset = super().get_queryset()
        for i, obj in enumerate(queryset, start=1):
            obj.serial_number = i
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_request_count = CustomerApplyRequest.objects.all().count()
        pending_count = PendingCustomerRequest.objects.all().count()
        pending_approval_count = PendingApprovalModel.objects.all().count()
        approved_count = ApprovedCustomerRequest.objects.all().count()
        rejected_count = RejectedCustomerRequest.objects.all().count()

        # Add counts to the context
        context["total_request_count"] = total_request_count
        context["pending_count"] = pending_count
        context["pending_approval_count"] = pending_approval_count
        context["approved_count"] = approved_count
        context["rejected_count"] = rejected_count

        return context


# cutomer reject request list
class CustomerRejectFormListView(ListView):
    model = RejectedCustomerRequest
    template_name = "main/All request/apply_list reject.html"
    context_object_name = "obj"  # Variable name used in the template
    queryset = RejectedCustomerRequest.objects.all().order_by("-update_at")
    paginate_by = 10  # Number of items to display per page

    def get_queryset(self):
        queryset = super().get_queryset()
        for i, obj in enumerate(queryset, start=1):
            obj.serial_number = i
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_request_count = CustomerApplyRequest.objects.all().count()
        pending_count = PendingCustomerRequest.objects.all().count()
        pending_approval_count = PendingApprovalModel.objects.all().count()
        approved_count = ApprovedCustomerRequest.objects.all().count()
        rejected_count = RejectedCustomerRequest.objects.all().count()

        # Add counts to the context
        context["total_request_count"] = total_request_count
        context["pending_count"] = pending_count
        context["pending_approval_count"] = pending_approval_count
        context["approved_count"] = approved_count
        context["rejected_count"] = rejected_count

        return context


# cutomer status change list
class ChangeStatusView(View):
    template_name = "main/All request/status.html"
    form_class = RequestRegistrationForm

    def get(self, request, request_id):
        customer_request = get_object_or_404(CustomerApplyRequest, id=request_id)
        form = self.form_class(instance=customer_request)
        return render(
            request,
            self.template_name,
            {"form": form, "customer_request": customer_request},
        )

    def post(self, request, request_id):
        customer_request = get_object_or_404(CustomerApplyRequest, id=request_id)
        form = self.form_class(request.POST, instance=customer_request)
        if form.is_valid():
            form.save()
            return redirect(
                "cutomer_form_list"
            )  # Redirect to a success page or any other page
        return render(
            request,
            self.template_name,
            {"form": form, "customer_request": customer_request},
        )


# cutomer  list
class AllCustomerListView(ListView):
    model = Customer
    template_name = "main/customer/all_customer.html"
    context_object_name = "customer"
    paginate_by = 10  # Set the number of items to display per page

    def get_queryset(self):
        queryset = Customer.objects.all()
        for i, obj in enumerate(queryset, start=1):
            obj.serial_number = i
        return queryset

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return redirect("main")
        return super().dispatch(request, *args, **kwargs)


# admin customer memebr profile view
class AdminCustomerDetailView(DetailView):
    model = Customer
    template_name = "main/customer/customer_profile_view.html"
    context_object_name = "customer"
    pk_url_kwarg = "pk"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect("main")
        return super().dispatch(request, *args, **kwargs)


# admin profile view
class AdminProfileView(DetailView):
    model = User
    template_name = "main/admin_profile.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        # This method is used to get the object for the view.
        # In this case, it returns the UserProfile related to the logged-in user.
        return self.request.user.user


# admin password change passoword
class AdminPasswordChangeView(PasswordChangeView):
    template_name = "main/admin/admin_password_change.html"
    success_url = reverse_lazy("main")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect("main")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Your password was successfully updated!")
        return super().form_valid(form)


# create a superuser
class CreateSuperuserView(View):
    template_name = "main/admin/create_admin.html"
    form_class = SuperuserCreationForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = True
            user.is_superuser = True
            user.save()
            # Log in the user
            login(request, user)
            messages.success(request, "SuperUser created successfully..!")
            return redirect(
                "main"
            )  # Change 'main' to the desired URL after superuser creation
        else:
            messages.error(request, "SuperUser creation failed. Please check the form.")
            return render(request, self.template_name, {"form": form})


# superuser list view
class SuperuserListView(ListView):
    model = User
    template_name = "main/superuser_list.html"
    context_object_name = "superusers"
    paginate_by = 10  # Set the number of items to display per page

    def get_queryset(self):
        queryset = User.objects.filter(is_superuser=True).order_by("-username")
        for i, obj in enumerate(queryset, start=1):
            obj.serial_number = i
        return queryset

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return redirect("main")
        return super().dispatch(request, *args, **kwargs)


# super user delete
class DeleteSuperAccountView(View):
    template_name = "main/admin/delete_account.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return redirect("main")  # Fixed typo here
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect("main")


# all service history
class ServiceListView(ListView):
    model = Service
    template_name = "main/service/service_list.html"
    context_object_name = "services"
    paginate_by = 10  # Set the number of items per page

    def get_queryset(self):
        queryset = Service.objects.all().order_by("-date_of_signature")
        for i, obj in enumerate(queryset, start=1):
            obj.serial_number = i
        return queryset

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return redirect("main")  # Fixed typo here
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Calculate total amount
        total_amount = Service.objects.all().count()

        # Add total_amount to the context
        context["total_amount"] = total_amount

        return context


# service create
class ServiceCreateView(CreateView):
    template_name = "main/service/service_form.html"
    form_class = ServiceForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return redirect("main")  # Fixed typo here
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Successfully Service/produc add..! ",
            )
            return redirect("service")
        else:
            messages.error(request, "Cannot submit your data. ")
            return render(
                request,
                self.template_name,
                {"form": form},
            )


# service view
class ServiceDetailView(DetailView):
    model = Service
    template_name = "main/service/service_profile_view.html"
    context_object_name = "service"
    pk_url_kwarg = "pk"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect("main")
        return super().dispatch(request, *args, **kwargs)


# serviuce update view
class ServiceEditView(UpdateView):
    model = Service
    template_name = "main/service/service_edit_view.html" 
    form_class = ServiceForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect("main")  # Change "main" to the appropriate URL or name
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        # Define the success URL after editing the service
        return reverse("service_view_detail", kwargs={"pk": self.object.pk})  # Change "service_detail" to the appropriate URL or name






# service delete
class ServiceDeleteView(DeleteView):
    model = Service  # Replace YourServiceModel with your actual model
    template_name = "main/service/service_confirm_delete.html"  # Customize the template as needed
    success_url = reverse_lazy("service")  # Replace "service" with your actual URL name

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return redirect("main")  # Redirect to the main page if not a superuser
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Successfully deleted the service/product.")
        return super().delete(request, *args, **kwargs)





