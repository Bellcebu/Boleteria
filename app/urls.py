from django.urls import path, include
from .views import (
    HomeView,
    EventListView,
    EventUpdateView,
    EventDeleteView,
    EventDetailView,
    LoginView,
    SignUpView,
    AuthView,
    LogOutView,
    TicketListView,
    CommentCreateView,
    RatingCreateView,
    NotificationDetailView,
    NotificationListView,
    UserProfileView,

    VenueCreateView,
    VenueUpdateView,
    VenueDeleteView,
    VenueListView,
    VenueDetailView,

    CategoryListView,
    CategoryDetailView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,

    TicketCreateView,
    RefundRequestListView,
    EventCreateView,
)


urlpatterns = [
    path('admin-panel/', include('admin_panel.urls')),

    path("", HomeView.as_view(), name="home"),

    path("events/", EventListView.as_view(), name="event_list"),
    path("events/<int:pk>/", EventDetailView.as_view(), name="event_detail"),
    path("events/nuevo/", EventCreateView.as_view(), name="event_crear"),  
    path("events/<int:pk>/editar/", EventUpdateView.as_view(), name="editar_evento"),
    path("events/<int:pk>/borrar/", EventDeleteView.as_view(), name="eliminar_evento"),
    path("events/<int:pk>/comment/", CommentCreateView.as_view(), name="add_comment"),
    path("events/<int:pk>/rating/", RatingCreateView.as_view(), name="add_rating"),
    path("events/<int:pk>/comprar/", TicketCreateView.as_view(), name="ticket_comprar"),  

    path('notificaciones/', NotificationListView.as_view(), name='notificaciones'),
    path('notificaciones/<int:pk>/', NotificationDetailView.as_view(), name='notification_detail'),

    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('auth/', AuthView.as_view(), name='auth'),
    path('logout/', LogOutView.as_view(), name='logout'),

    path('users/<str:username>/', UserProfileView.as_view(), name='user_profile'),

    path('tickets/', TicketListView.as_view(), name='ticket_list'),

    path("venues/", VenueListView.as_view(), name="venue_listar"),
    path("venues/nuevo/", VenueCreateView.as_view(), name="venue_crear"),
    path("venues/<int:pk>/", VenueDetailView.as_view(), name="venue_detalle"),
    path("venues/<int:pk>/editar/", VenueUpdateView.as_view(), name="venue_editar"),
    path("venues/<int:pk>/borrar/", VenueDeleteView.as_view(), name="venue_borrar"),

    path("categories/", CategoryListView.as_view(), name="category_listar"),
    path("categories/nuevo/", CategoryCreateView.as_view(), name="category_crear"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category_detalle"),
    path("categories/<int:pk>/editar/", CategoryUpdateView.as_view(), name="category_editar"),
    path("categories/<int:pk>/borrar/", CategoryDeleteView.as_view(), name="category_borrar"),

    path('refund-requests/', RefundRequestListView.as_view(), name='refund_request_listar'),
]