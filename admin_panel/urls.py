from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('crear-evento/', views.AdminEventCreateView.as_view(), name='admin_event_create'),
    path('crear-categoria/', views.AdminCategoryCreateView.as_view(), name='admin_category_create'),
    path('roles/', views.user_roles_list, name='admin_user_roles'),
    path('roles/asignar/<int:user_id>/', views.assign_role, name='admin_assign_role'),
]