from django.urls import path, include
from .views import (
    HomeView,
    EventListView,
    EventDetailView,
    CommentCreateView,
    RatingCreateView,
    TicketCreateView,
    TicketListView,
    TicketDetailView,
    NotificationListView,
    NotificationDetailView,
    LoginView,
    SignUpView,
    AuthView,
    LogOutView,
    UserProfileView,
    VenueListView,
    VenueDetailView,
    CategoryListView,
    CategoryDetailView,
    CommentListView,
    CommentDeleteView,
    CommentDetailView,
    CommentUpdateView,
)

urlpatterns = [
    # --- Admin ---
    path('admin-panel/', include('admin_panel.urls')),

    # --- Home ---
    path('', HomeView.as_view(), name='home'),

    # --- Eventos ---
    path('events/', EventListView.as_view(), name='event_list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('events/<int:pk>/rating/', RatingCreateView.as_view(), name='add_rating'),
    path('events/<int:event_pk>/comprar/<int:tier_id>/', TicketCreateView.as_view(), name='ticket_buy'),

    # --- Tickets ---
    path('tickets/', TicketListView.as_view(), name='ticket_list'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),

    # --- Notificaciones ---
    path('notificaciones/', NotificationListView.as_view(), name='notificaciones'),
    path('notificaciones/<int:pk>/', NotificationDetailView.as_view(), name='notification_detail'),

    # --- Autenticación ---
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('auth/', AuthView.as_view(), name='auth'),
    path('logout/', LogOutView.as_view(), name='logout'),

    # --- Usuarios ---
    path('users/<str:username>/', UserProfileView.as_view(), name='user_profile'),

    # --- Venues ---
    path('venues/', VenueListView.as_view(), name='venue_listar'),
    path('venues/<int:pk>/', VenueDetailView.as_view(), name='venue_detalle'),

    # --- Categorías ---
    path('categories/', CategoryListView.as_view(), name='category_listar'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detalle'),

    #comentarios
    path('eventos/<int:pk>/comentarios/', CommentListView.as_view(), name='comentario_listar'),
    path('eventos/<int:pk_event>/comentarios/<int:pk/>', CommentDetailView.as_view(), name='comentario_detalle'),
    path('events/<int:pk_event>/comentarios/crear/', CommentCreateView.as_view(), name='comentario_crear'),
    path('events/<int:pk_event>/comentarios/<int:pk>/editar/', CommentUpdateView.as_view(), name='comentario_editar'),
    path('events/<int:pk_event>/comentarios/<int:pk>/borrar/', CommentDeleteView.as_view(), name='comentario_borrar'),
]

