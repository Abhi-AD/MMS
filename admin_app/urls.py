from django.urls import path
from admin_app import views
from admin_app.views import *

urlpatterns = [
    path('', PaymentCreateView.as_view(), name='payment'),
    path("payment_history/", PaymentListView.as_view(), name="payment_history")
    
]
