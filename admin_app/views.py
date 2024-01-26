from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import  View, ListView, CreateView
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages


from admin_app.models import *
from app.models import *
from admin_app.forms import PaymentForm, RequestRegistrationForm

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




class PaymentListView(ListView):
    model = Payment
    template_name = "main/payment_list.html"

    def get_queryset(self):
        return Payment.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calculate total amount
        total_amount = Payment.objects.aggregate(total_amount=models.Sum('amount'))['total_amount']
        
        # Add total_amount to the context
        context['total_amount'] = total_amount

        return context
    


class PaymentCreateView(CreateView):
    template_name = 'main/payment_form.html'
    form_class = PaymentForm
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Successfully submitted your query. We will transaction you soon "
            )
            return redirect("payment_history")
        else:
            messages.error(request, "Cannot submit your data. ")
            return render(
                request,
                self.template_name,
                {"form": form},
            )

# views.py
class ChangeStatusView(View):
    template_name = 'status.html'
    form_class = RequestRegistrationForm

    def get(self, request, request_id):
        customer_request = get_object_or_404(CustomerApplyRequest, id=request_id)
        form = self.form_class(instance=customer_request)
        return render(request, self.template_name, {'form': form, 'customer_request': customer_request})

    def post(self, request, request_id):
        customer_request = get_object_or_404(CustomerApplyRequest, id=request_id)
        form = self.form_class(request.POST, instance=customer_request)
        if form.is_valid():
            form.save()
            return redirect('cutomer_form_list')  # Redirect to a success page or any other page
        return render(request, self.template_name, {'form': form, 'customer_request': customer_request})




class AdminLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("main")  

class CustomerFormListView(ListView):
    model = CustomerApplyRequest
    template_name = 'main/All request/apply_list.html'
    context_object_name = 'obj'  # Variable name used in the template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        pending_count = CustomerApplyRequest.objects.filter(status='pending').count()
        pending_approval_count = CustomerApplyRequest.objects.filter(status='pending_approval').count()
        approved_count = CustomerApplyRequest.objects.filter(status='approved').count()
        rejected_count = CustomerApplyRequest.objects.filter(status='rejected').count()

        # Add counts to the context
        context['pending_count'] = pending_count
        context['pending_approval_count'] = pending_approval_count
        context['approved_count'] = approved_count
        context['rejected_count'] = rejected_count

        return context  



class ChangeStatusView(View):
    template_name = 'main/All request/status.html'
    form_class = RequestRegistrationForm

    def get(self, request, request_id):
        customer_request = get_object_or_404(CustomerApplyRequest, id=request_id)
        form = self.form_class(instance=customer_request)
        return render(request, self.template_name, {'form': form, 'customer_request': customer_request})

    def post(self, request, request_id):
        customer_request = get_object_or_404(CustomerApplyRequest, id=request_id)
        form = self.form_class(request.POST, instance=customer_request)
        if form.is_valid():
            form.save()
            return redirect('cutomer_form_list')  # Redirect to a success page or any other page
        return render(request, self.template_name, {'form': form, 'customer_request': customer_request})



class CustomerPendingFormListView(ListView):
    model = PendingCustomerRequest
    template_name = 'main/All request/apply_list pending.html'
    context_object_name = 'obj'  # Variable name used in the template
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Count the status types
        pending_count = CustomerApplyRequest.objects.filter(status='pending').count()
        pending_approval_count = CustomerApplyRequest.objects.filter(status='pending_approval').count()
        approved_count = CustomerApplyRequest.objects.filter(status='approved').count()
        rejected_count = CustomerApplyRequest.objects.filter(status='rejected').count()

        # Add counts to the context
        context['pending_count'] = pending_count
        context['pending_approval_count'] = pending_approval_count
        context['approved_count'] = approved_count
        context['rejected_count'] = rejected_count

        return context  



class CustomerPendingApprovalFormListView(ListView):
    model = PendingApprovalModel
    template_name = 'main/All request/apply_list pending approval.html'
    context_object_name = 'obj'  # Variable name used in the template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Count the status types
        pending_count = CustomerApplyRequest.objects.filter(status='pending').count()
        pending_approval_count = CustomerApplyRequest.objects.filter(status='pending_approval').count()
        approved_count = CustomerApplyRequest.objects.filter(status='approved').count()
        rejected_count = CustomerApplyRequest.objects.filter(status='rejected').count()

        # Add counts to the context
        context['pending_count'] = pending_count
        context['pending_approval_count'] = pending_approval_count
        context['approved_count'] = approved_count
        context['rejected_count'] = rejected_count

        return context  


class CustomerApprovalFormListView(ListView):
    model = ApprovedCustomerRequest
    template_name = 'main/All request/apply_list approval.html'
    context_object_name = 'obj'  # Variable name used in the template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Count the status types
        pending_count = CustomerApplyRequest.objects.filter(status='pending').count()
        pending_approval_count = CustomerApplyRequest.objects.filter(status='pending_approval').count()
        approved_count = CustomerApplyRequest.objects.filter(status='approved').count()
        rejected_count = CustomerApplyRequest.objects.filter(status='rejected').count()

        # Add counts to the context
        context['pending_count'] = pending_count
        context['pending_approval_count'] = pending_approval_count
        context['approved_count'] = approved_count
        context['rejected_count'] = rejected_count

        return context  




class CustomerRejectFormListView(ListView):
    model = RejectedCusomerRequest
    template_name = 'main/All request/apply_list reject.html'
    context_object_name = 'obj'  # Variable name used in the template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Count the status types
        pending_count = CustomerApplyRequest.objects.filter(status='pending').count()
        pending_approval_count = CustomerApplyRequest.objects.filter(status='pending_approval').count()
        approved_count = CustomerApplyRequest.objects.filter(status='approved').count()
        rejected_count = CustomerApplyRequest.objects.filter(status='rejected').count()

        # Add counts to the context
        context['pending_count'] = pending_count
        context['pending_approval_count'] = pending_approval_count
        context['approved_count'] = approved_count
        context['rejected_count'] = rejected_count

        return context  












