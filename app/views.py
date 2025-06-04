from django.views.generic import TemplateView, ListView, DetailView
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from .forms import (
    SignUpForm,
    CommentForm,
    RatingForm,
)
from .models import (
    Event,
    Ticket,
    RefundRequest,
    Comment,
    Notificacion,
)

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        return context


class EventListView(ListView):
    model = Event
    template_name = "app/events.html"
    context_object_name = "events"

    def get_queryset(self):
        return Event.objects.all().order_by("date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = "app/event_detail.html"
    context_object_name = "event"


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        return render(request, 'login.html', {'form': form})
    
class LogOutView(View):
    def get(self,request):
        logout(request)
        return redirect('login')
        
class SignUpView(View):
    def get(self, request):
        form = SignUpForm()  
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():  
            user = form.save()
            login(request, user)
            return redirect('home')  
        return render(request, 'signup.html', {'form': form})
    
class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = "app/tickets.html"
    context_object_name = "tickets"

    def get_queryset(self):
        return Ticket.objects.filter(user_fk=self.request.user).order_by("-buy_date")

    def post(self, request, *args, **kwargs):
        ticket_id = request.POST.get('ticket_id')
        reason = request.POST.get('reason')

        if not reason:
            messages.error(request, "Por favor, proporciona un motivo para el reembolso.")
            return redirect('tickets')

        ticket = get_object_or_404(Ticket, ticket_code=ticket_id, user_fk=request.user)

        existing_request = RefundRequest.objects.filter(ticket_code=ticket.ticket_code).first()
        if existing_request:
            messages.error(request, "Ya solicitaste un reembolso para este ticket.")
        else:
            RefundRequest.new(user=request.user, ticket_code=ticket.ticket_code, reason=reason)
            messages.success(request, "Tu solicitud de reembolso fue enviada con éxito.")

        return redirect('tickets')

class UserProfileView(LoginRequiredMixin,View):

    def get(self, request, username):
        user_profile = get_object_or_404(User, username=username)
        return render(request, 'users/profile.html', {'profile_user': user_profile})
    
class CommentCreateView(View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.event = event
            comment.user = request.user
            comment.save()
            return redirect('event_detail', pk=pk)

        return render(request, 'events/event_detail.html', {
            'event': event,
            'form': form,
        })
    
class RatingCreateView(View):

    def post(self,request,pk):
        event = get_object_or_404(Event,pk=pk)
        form = RatingForm(request.POST)

        if form.is_valid():
            rating = form.save(commit=False)
            rating.user_fk=request.user
            rating.event=event
            rating.save()
            return redirect('event_detail', pk=pk)

        return render(request, 'events/event_detail.html', {
            'event': event,
            'form': form,
        })
    
class NotificationListView(LoginRequiredMixin, ListView):
    model = Notificacion
    template_name = 'app/notificaciones.html'   
    context_object_name = 'notificaciones'  

    def get_queryset(self):
        return Notificacion.objects.filter(users=self.request.user).order_by('-created_at')

    def post(self, request, *args, **kwargs):
        notificacion_id = request.POST.get('notification_id')

        if notificacion_id:
            notification = get_object_or_404(Notificacion, pk=notificacion_id, users=request.user)
            notification.is_read = True
            notification.save()
            messages.success(request, 'Notificación marcada como leída.')
        else:
            messages.error(request, 'ID de notificación no válido.')

        return redirect('notificationes')
    

class NotificationDetailView(DetailView):
    model = Notificacion
    template_name = "app/notification_detail.html"
    context_object_name = "notificacion"
    
