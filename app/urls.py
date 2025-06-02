from django.urls import path
from .views import (
    HomeView,
    EventListView,
    EventDetailView,
    LoginView, 
    SignUpView,
    LogOutView,
    ticketListView,
    CommentCreateView,
    RatingCreateView,
    NotificationDetailView,
    NotificationListView,
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
    path('tickets/',ticketListView.as_view(), name='ticket'),
    path('events/<int:pk>/comment/', CommentCreateView.as_view(), name='add_comment'),
    path('events/<int:pk>/rating/', RatingCreateView.as_view(), name='add_rating'),
]