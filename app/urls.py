from django.urls import path
from .views import (
    HomeView,
    EventListView,
    EventDetailView,
    LoginView, 
    SignUpView,
    LogOutView,
    TicketListView,
    CommentCreateView,
    RatingCreateView,
    NotificationDetailView,
    NotificationListView,

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

)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("events/", EventListView.as_view(), name="events"),
    path("events/<int:pk>/", EventDetailView.as_view(), name="event_detail"),
    path('notificaciones/',NotificationListView.as_view(), name = 'notificaciones' ),
    path('notificaciones/<int:pk>', NotificationDetailView.as_view(), 'notification_detail'),    
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/',LogOutView.as_view(),name='logout'),
    path('tickets/',TicketListView.as_view(), name='ticket'),
    path('events/<int:pk>/comment/', CommentCreateView.as_view(), name='add_comment'),
    path('events/<int:pk>/rating/', RatingCreateView.as_view(), name='add_rating'),

    path("venues/", VenueListView.as_view(), name="venue_listar"),
    path("venues/nuevo", VenueCreateView.as_view(), name="venue_crear"),
    path("venues/<int>:pk", VenueDetailView.as_view(), name= "venue_detalle"),
    path("venues/<int>:pk/editar/", VenueUpdateView.as_view(), name="venue_editar"),
    path("venues/<int>:pk/borrar/", VenueDeleteView.as_view(), name="venue_borrar"),

    path("categories/", VenueListView.as_view(), name="category_listar"),
    path("categories/nuevo", CategoryCreateView.as_view(), name="category_crear"),
    path("categories/<int>:pk", CategoryDetailView.as_vieww(), name="category_detalle"),
    path("categories/<int>:pk", CategoryUpdateView.as_view(), name="category_editar"),
    path("categories/<int>:pk", CategoryDeleteView.as_view(), name="category_borrar"),
]