from django.urls import path, include
from .views import (
    HomeView,
    EventListView,
    EventDetailView,
    CommentCreateView,
    RatingCreateView,
    TicketPurchaseView,
    TicketListView,
    FavoriteListView,
    TicketDetailView,
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
    CommentDetailView,
    RatingCreateView,
    RatingUpdateView,
    RatingDeleteView,
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
    path('events/<int:event_id>/comprar/<int:tier_id>/', TicketPurchaseView.as_view(), name='ticket_purchase'),

    # --- Tickets ---
    path('tickets/', TicketListView.as_view(), name='ticket_list'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket_detail'),

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
    path('events/<int:pk>/comentarios/', CommentListView.as_view(), name='comentary_list'),
    path('events/<int:pk_event>/comentarios/<int:pk>/', CommentDetailView.as_view(), name='comentary_detail'),
    path('events/<int:pk_event>/comentarios/crear/', CommentCreateView.as_view(), name='comentary_create'),

    path('favoritos/', FavoriteListView.as_view(), name='favorite_list'),
    path('events/<int:pk_event>/rating/crear/', RatingCreateView.as_view(), name='rating_crear'),
    path('rating/<int:pk>/editar/', RatingUpdateView.as_view(), name='rating_editar'),
    path('rating/<int:pk>/borrar/', RatingDeleteView.as_view(), name='rating_borrar'),


]

