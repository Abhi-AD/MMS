from django.urls import path
from admin_app import views
from admin_app.views import *

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('payment/', PaymentCreateView.as_view(), name='payment'),
    path("payment_history/", PaymentListView.as_view(), name="payment_history"),
    path("main_logout/", AdminLogoutView.as_view(), name="main_logout"),
    path('cutomer_form_list/', CustomerFormListView.as_view(), name='cutomer_form_list'),
    path('change_status/<int:request_id>/', ChangeStatusView.as_view(), name='change_status'),
    
]
