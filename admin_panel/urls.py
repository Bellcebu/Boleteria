from django.urls import path
from . import views

urlpatterns = [
    path('', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('reembolsos/', views.RefundListView.as_view(), name='admin_reembolsos'),
    path('reembolsos/<int:pk>/<str:action>/', views.RefundActionView.as_view(), name='refund_action'),
]
