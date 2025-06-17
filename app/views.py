from django.views.generic import TemplateView, ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from datetime import datetime, time
from django.utils import timezone

from .forms import (
    SignUpForm,
    CommentForm,
    RatingForm,
    TicketModelForm,
    VenueModelForm,
    CategoryModelForm,
    EventModelForm,
)
from .models import (
    Event,
    Ticket,
    RefundRequest,
    Comment,
    Profile,
    Notificacion,
    Venue,
    Category,
)

# ===== 1. HOME Y AUTENTICACIÓN =====
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['eventos'] = Event.objects.all().order_by('-date')[:6]
        return context

class AuthView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        signup_form = SignUpForm()
        return render(request, 'auth.html', {'login_form': login_form, 'signup_form': signup_form})

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'auth.html', {'form': form})
    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('home')
        messages.error(request, "Credenciales inválidas. Intenta nuevamente.")
        return render(request, 'auth.html', {'form': form})

class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'auth.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('home')
        return render(request, 'auth.html', {'form': form})
    
# ===== 2. EVENTOS (solo listar y detalle) =====
class EventListView(ListView):
    model = Event
    template_name = "app/event/event_list.html"
    context_object_name = "eventos"
    paginate_by = 10

    def get_queryset(self):
        queryset = Event.objects.all().order_by("date")
        categoria_id = self.request.GET.get('categoria')
        fecha_desde = self.request.GET.get('fecha_desde')
        fecha_hasta = self.request.GET.get('fecha_hasta')
        if categoria_id:
            queryset = queryset.filter(category_id=categoria_id)
        if fecha_desde:
            try:
                dt = datetime.strptime(fecha_desde, '%Y-%m-%d')
                dt = timezone.make_aware(datetime.combine(dt.date(), time.min))
                queryset = queryset.filter(date__gte=dt)
            except ValueError:
                pass
        if fecha_hasta:
            try:
                dt = datetime.strptime(fecha_hasta, '%Y-%m-%d')
                dt = timezone.make_aware(datetime.combine(dt.date(), time.max))
                queryset = queryset.filter(date__lte=dt)
            except ValueError:
                pass
        return queryset

class EventDetailView(DetailView):
    model = Event
    template_name = "app/event/event_detail.html"
    context_object_name = "event"

# ===== 3. COMENTARIOS Y VALORACIONES =====
class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.event = event
            comment.user = request.user
            comment.save()
            return redirect('event_detail', pk=pk)
        return render(request, 'app/event/event_detail.html', {'event': event, 'form': form})

class RatingCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user_fk = request.user
            rating.event = event
            rating.save()
            return redirect('event_detail', pk=pk)
        return render(request, 'app/event/event_detail.html', {'event': event, 'form': form})

# ===== 4. TICKETS =====
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
            return redirect('ticket_list')
        ticket = get_object_or_404(Ticket, ticket_code=ticket_id, user_fk=request.user)
        if RefundRequest.objects.filter(ticket_code=ticket.ticket_code).exists():
            messages.error(request, "Ya solicitaste un reembolso para este ticket.")
        else:
            RefundRequest.new(user=request.user, ticket_code=ticket.ticket_code, reason=reason)
            messages.success(request, "Tu solicitud de reembolso fue enviada con éxito.")
        return redirect('ticket_list')

class TicketDetailView(DetailView):
    model = Ticket
    template_name = "ticket/ticket_detail.html"
    context_object_name = "ticket"

class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketModelForm
    template_name = "ticket/ticket_form.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['evento'] = get_object_or_404(Event, pk=self.kwargs['pk'])
        return context
    def form_valid(self, form):
        ticket = form.save(commit=False)
        ticket.user_fk = self.request.user
        ticket.event_fk = get_object_or_404(Event, pk=self.kwargs['pk'])
        ticket.save()
        messages.success(self.request, "¡Tu entrada fue comprada con éxito!")
        return redirect('event_detail', pk=self.kwargs['pk'])

# ===== 5. PERFIL Y NOTIFICACIONES =====
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .forms import ProfileImageForm

@method_decorator(login_required, name='dispatch')
class UserProfileView(View):
    def get(self, request, username):
        profile_user = get_object_or_404(User, username=username)
        form = None
        if request.user == profile_user:
            form = ProfileImageForm(instance=profile_user.profile)
        return render(request, 'users/profile.html', {'profile_user': profile_user, 'form': form})

    def post(self, request, username):
        profile_user = get_object_or_404(User, username=username)
        if request.user != profile_user:
            messages.error(request, "No tienes permiso para modificar este perfil.")
            return redirect('user_profile', username=username)

        form = ProfileImageForm(request.POST, request.FILES, instance=profile_user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Foto de perfil actualizada.")
            return redirect('user_profile', username=username)
        messages.error(request, "Hubo un error al subir la imagen.")
        return render(request, 'users/profile.html', {'profile_user': profile_user, 'form': form})


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notificacion
    template_name = 'app/notificacion/notificaciones.html'
    context_object_name = 'notificaciones'
    def get_queryset(self):
        return Notificacion.objects.filter(users=self.request.user).order_by('-created_at')
    def post(self, request, *args, **kwargs):
        notification_id = request.POST.get('notification_id')
        if notification_id:
            notification = get_object_or_404(Notificacion, pk=notification_id, users=request.user)
            notification.is_read = True
            notification.save()
            messages.success(request, 'Notificación marcada como leída.')
        else:
            messages.error(request, 'ID de notificación no válido.')
        return redirect('notificaciones')

class NotificationDetailView(DetailView):
    model = Notificacion
    template_name = "app/notificacion/notification_detail.html"
    context_object_name = "notificacion"

# ===== 6. VENUES (listar y detalle) =====
class VenueListView(ListView):
    model = Venue
    template_name = 'venue/venue_list.html'
    context_object_name = 'venues'
    paginate_by = 10

class VenueDetailView(DetailView):
    model = Venue
    template_name = "venue/venue_detalle.html"
    context_object_name = "venue"

# ===== 7. CATEGORÍAS (listar y detalle) =====
class CategoryListView(ListView):
    model = Category
    template_name = "category/category_list.html"
    context_object_name = "categories"

class CategoryDetailView(DetailView):
    model = Category
    template_name = "category/category_detail.html"
    context_object_name = "category"