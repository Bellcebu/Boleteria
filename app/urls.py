from django.urls import path
from .views import (
    HomeView,
    EventListView,
    EventDetailView,
    LoginView, 
    SignUpView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("events/", EventListView.as_view(), name="events"),
    path("events/<int:pk>/", EventDetailView.as_view(), name="event_detail"),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('historial/', SignUpView.as_view(), name='historial'),
    path('user/', SignUpView.as_view(), name='user'),
]