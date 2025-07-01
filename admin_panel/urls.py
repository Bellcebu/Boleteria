from django.urls import path
from . import views
from .views import(
    AdminNotificationListView,
    AdminNotificationCreateView,
    AdminNotificationUpdateView,
    AdminNotificationDeleteView,
    AdminNotificationDetailView,
)

urlpatterns = [
    path('', views.AdminHomeView.as_view(), name='admin_home'),
    path('vendedor/', views.VendedorHomeView.as_view(), name='vendedor_home'),

    # --- Herramientas ---
    path('eventos/', views.AdminEventView.as_view(), name='event'),
    path('eventos/<int:event_id>/tickets/', views.AdminEventTicketsView.as_view(), name='event_tickets'),
    path('categories/', views.AdminCategoriesView.as_view(), name='categories'),
    path('venues/', views.AdminVenueView.as_view(), name='venue'),
    path('refund-requests/', views.AdminRefundRequesView.as_view(), name='refund_request'),
    path('rols/', views.AdminRolsView.as_view(), name='rols'),
    path('comments/', views.AdminCommentsView.as_view(), name='comments'),
    path('promotions/', views.AdminPromotionsView.as_view(), name='promotions'),
    

  # --- notification ---
    path('notifications/', AdminNotificationListView.as_view(), name='notification_list'),
    path('notifications/create/', AdminNotificationCreateView.as_view(), name='notification_create'),
    path('notifications/<int:pk>/', AdminNotificationDetailView.as_view(), name='notification_detail'),
    path('notifications/<int:pk>/edit/', AdminNotificationUpdateView.as_view(), name='notification_edit'),
    path('notifications/<int:pk>/delete/', AdminNotificationDeleteView.as_view(), name='notification_delete'),

    # --- Vendedor ---

    
    

]
