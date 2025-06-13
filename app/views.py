from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from .forms import (
    SignUpForm,
    CommentForm,
    RatingForm,
    VenueModelForm,
    CategoryModelForm,
    TicketModelForm,
    EventModelForm,
)
from .models import (
    Event,
    Ticket,
    RefundRequest,
    Comment,
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
        return render(request, 'auth.html', {
            'login_form': login_form,
            'signup_form': signup_form,
        })


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
            else:
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
            login(request, user)
            return redirect('home')
        return render(request, 'auth.html', {'form': form})


# ===== 2. EVENTOS =====
class EventListView(ListView):
    model = Event
    template_name = "app/event/events.html"
    context_object_name = "events"

    def get_queryset(self):
        return Event.objects.all().order_by("date")


class EventDetailView(DetailView):
    model = Event
    template_name = "app/event/event_detail.html"
    context_object_name = "event"


class EventCreateView(CreateView):
    model = Event
    form_class = EventModelForm
    template_name = 'app/event/event_form.html'
    success_url = reverse_lazy('event_listar')

    def form_valid(self, form):
        messages.success(self.request, "El evento fue creado con éxito.")
        return super().form_valid(form)


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


# ===== 3. TICKETS Y REEMBOLSOS =====
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


class TicketDetailView(DetailView):
    model = Ticket
    template_name = "ticket/ticket_detail.html"
    context_object_name = "ticket"


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketModelForm
    template_name = "ticket/ticket_form.html"

    def form_valid(self, form):
        ticket = form.save(commit=False)
        ticket.user_fk = self.request.user
        ticket.event_fk = get_object_or_404(Event, pk=self.kwargs['pk'])
        ticket.save()
        messages.success(self.request, "¡Tu entrada fue comprada con éxito!")
        return redirect("event_detail", pk=self.kwargs['pk'])


class RefundRequestListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = RefundRequest
    template_name = 'refund_request/refund_request_list_admin.html'
    context_object_name = 'refund_request_admin'
    permission_required = 'can_view_refund_request'

    def get_queryset(self):
        return RefundRequest.objects.all().order_by('-created_at')


# ===== 4. PERFIL DE USUARIO =====
class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, username):
        user_profile = get_object_or_404(User, username=username)
        return render(request, 'users/profile.html', {'profile_user': user_profile})


# ===== 5. NOTIFICACIONES =====
class NotificationListView(LoginRequiredMixin, ListView):
    model = Notificacion
    template_name = 'app/notificacion/notificaciones.html'
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
    template_name = "app/notificacion/notification_detail.html"
    context_object_name = "notificacion"


# ===== 6. VENUES CRUD =====
class VenueListView(ListView):
    model = Venue
    template_name = 'venue/venues.html'
    context_object_name = 'venues'
    paginate_by = 10


class VenueCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Venue
    form_class = VenueModelForm
    template_name = 'venue/venue_form.html'
    success_url = reverse_lazy('venue_listar')
    permission_required = "can_create_venue"

    def form_valid(self, form):
        venue = form.save(commit=False)
        venue.save()
        messages.success(self.request, f'El venue {venue.name} fue creado correctamente.')
        return super().form_valid(form)


class VenueUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Venue
    form_class = VenueModelForm
    template_name = 'venue/venue_form.html'
    success_url = reverse_lazy('venue_listar')
    permission_required = "can_update_venue"

    def form_valid(self, form):
        venue = form.save(commit=False)
        venue.save()
        messages.success(self.request, f'El venue {venue.name} fue actualizado con éxito.')
        return super().form_valid(form)


class VenueDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Venue
    template_name = 'venue/venue_form.html'
    success_url = reverse_lazy('venue_listar')
    permission_required = "can_delete_venue"


class VenueDetailView(DetailView):
    model = Venue
    template_name = "venue/venue_detalle.html"
    context_object_name = "venue"


# ===== 7. CATEGORÍAS CRUD =====
class CategoryListView(ListView):
    model = Category
    template_name = "category/category_list.html"
    context_object_name = "categories"


class CategoryDetailView(DetailView):
    model = Category
    template_name = "category/category_detail.html"
    context_object_name = "category"


class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Category
    form_class = CategoryModelForm
    template_name = "category/category_form.html"
    success_url = reverse_lazy("category_listar")
    permission_required = "can_create_category"

    def form_valid(self, form):
        category = form.save(commit=False)
        category.save()
        messages.success(self.request, f"La categoría {category.name} fue creada con éxito.")
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryModelForm
    template_name = "category/category_form.html"
    success_url = reverse_lazy("category_listar")
    permission_required = "can_update_category"

    def form_valid(self, form):
        category = form.save(commit=False)
        category.save()
        messages.success(self.request, f"La categoría {category.name} fue editada con éxito.")
        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Category
    template_name = "category/category_confirm_delete.html"
    success_url = reverse_lazy("category_listar")
    permission_required = "can_delete_category"
