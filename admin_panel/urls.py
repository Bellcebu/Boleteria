from django.urls import path
from . import views

urlpatterns = [
    # --- Dashboard ---
    path('', views.admin_dashboard, name='admin_dashboard'),

    # --- Eventos ---
    path('events/crear/', views.EventCreateView.as_view(), name='event_create'),
    path('events/<int:pk>/editar/', views.EventUpdateView.as_view(), name='event_edit'),
    path('events/<int:pk>/borrar/', views.EventDeleteView.as_view(), name='event_delete'),

    # --- Categorías ---
    path('categories/crear/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/editar/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/borrar/', views.CategoryDeleteView.as_view(), name='category_delete'),

    # --- Venues ---
    path('venues/crear/', views.VenueCreateView.as_view(), name='venue_create'),
    path('venues/<int:pk>/editar/', views.VenueUpdateView.as_view(), name='venue_edit'),
    path('venues/<int:pk>/borrar/', views.VenueDeleteView.as_view(), name='venue_delete'),

    # --- Solicitudes de reembolso ---
    path('refund-requests/', views.RefundRequestListView.as_view(), name='refund_request_list'),

    # --- Roles ---
    path('roles/', views.user_roles_list, name='user_roles'),
    path('roles/asignar/<int:user_id>/', views.assign_role, name='assign_role'),
]
