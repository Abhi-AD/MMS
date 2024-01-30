from django.urls import path
from admin_app import views
from admin_app.views import *

urlpatterns = [
    path("", MainView.as_view(), name="main"),
    path("all_customer/", AllCustomerListView.as_view(), name="all_customer"),
    path("payment/", PaymentCreateView.as_view(), name="payment"),
    path("payment_history/", PaymentListView.as_view(), name="payment_history"),
    path("main_logout/", AdminLogoutView.as_view(), name="main_logout"),
    path(
        "cutomer_form_list/", CustomerFormListView.as_view(), name="cutomer_form_list"
    ),
    path(
        "cutomer_pendling_list/",
        CustomerPendingFormListView.as_view(),
        name="cutomer_pendling_list",
    ),
    path(
        "cutomer_pendling_approval_list/",
        CustomerPendingApprovalFormListView.as_view(),
        name="cutomer_pendling_approval_list",
    ),
    path(
        "cutomer_approval_list/",
        CustomerApprovalFormListView.as_view(),
        name="cutomer_approval_list",
    ),
    path(
        "cutomer_reject_list/",
        CustomerRejectFormListView.as_view(),
        name="cutomer_reject_list",
    ),
    path(
        "change_status/<int:request_id>/",
        ChangeStatusView.as_view(),
        name="change_status",
    ),
    path(
        "customer/<int:pk>/",
        AdminCustomerDetailView.as_view(),
        name="admin_customer_view_detail",
    ),
    path(
        "admin_password_change/",
        AdminPasswordChangeView.as_view(),
        name="admin_password_change",
    ),
    path("admin_profile/", AdminProfileView.as_view(), name="admin_profile"),
    path("create_superuser/", CreateSuperuserView.as_view(), name="create_superuser"),
    path("superuser_list/", SuperuserListView.as_view(), name="superuser_list"),
    path(
        "delete_super_account/",
        DeleteSuperAccountView.as_view(),
        name="delete_super_account",
    ),
    path("service/", ServiceListView.as_view(), name="service"),
    path("service_create/", ServiceCreateView.as_view(), name="service_create"),
    path(
        "service/<int:pk>/",
        ServiceDetailView.as_view(),
        name="service_view_detail",
    ),
    path("service/<int:pk>/edit/", ServiceEditView.as_view(), name="service_edit"),
    path(
        "service/<int:pk>/delete/", ServiceDeleteView.as_view(), name="service-delete"
    ),
]
