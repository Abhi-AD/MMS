from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View, ListView, CreateView
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse,reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.views import View
from django.contrib import messages

from django.db.models import Count
from django.utils import timezone

from admin_app.models import *
from app.models import *
from admin_app.forms import PaymentForm

# create the view
class PaymentListView(ListView):
    model = Payment
    template_name = "app/payment_list.html"

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
    template_name = 'admin/payment_form.html'
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