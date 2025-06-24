from django.views.generic import TemplateView, ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import login, logout
from admin_panel.views import is_admin
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from datetime import datetime, time
from django.utils import timezone
from django.urls import reverse_lazy

from .forms import (
    SignUpForm,
    CommentForm,
    RatingForm,
    TicketPurchaseForm,
    TicketModelForm,
    VenueModelForm,
    CategoryModelForm,
    EventModelForm,
    ProfileImageForm,
    RefundRequestForm,
)
from .models import (
    Event,
    Ticket,
    RefundRequest,
    TicketTier,
    Comment,
    Profile,
    Notification,
    Venue,
    Category,
)

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_events_for_user(self, user):  
        if user.is_staff or user.groups.filter(name='Vendedor').exists():
            return Event.objects.all()  
        else:
            return Event.objects.filter(date__gte=timezone.now())
    
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['eventos'] = self.get_events_for_user(self.request.user)
        return context 


class AuthView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        signup_form = SignUpForm()
        return render(request, 'auth.html', {'login_form': login_form, 'signup_form': signup_form})

class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        signup_form = SignUpForm()
        return render(request, 'auth.html', {
            'login_form': login_form,
            'signup_form': signup_form,
            'active_form': 'login',
        })

    def post(self, request):
        login_form = AuthenticationForm(request, data=request.POST)
        signup_form = SignUpForm()
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('home')
        messages.error(request, "Credenciales inválidas. Intenta nuevamente.")
        return render(request, 'auth.html', {
            'login_form': login_form,
            'signup_form': signup_form,
            'active_form': 'login',
        })


class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

class SignUpView(View):
    def get(self, request):
        signup_form = SignUpForm()
        login_form = AuthenticationForm()
        return render(request, 'auth.html', {
            'signup_form': signup_form,
            'login_form': login_form,
            'active_form': 'signup',
        })

    def post(self, request):
        signup_form = SignUpForm(request.POST)
        login_form = AuthenticationForm()
        
        if signup_form.is_valid():
            user = signup_form.save()
            Profile.objects.create(user=user)
            login(request, user)  
            messages.success(request, "¡Registro exitoso! Bienvenido a EventApp.")
            return redirect('home')
        
        return render(request, 'auth.html', {
            'signup_form': signup_form,
            'login_form': login_form,
            'active_form': 'signup',  
        })


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['es_admin'] = is_admin(self.request.user)
        context['categorias'] = Category.objects.all()
        context['categoria_seleccionada'] = self.request.GET.get('categoria', '')
        context['fecha_desde'] = self.request.GET.get('fecha_desde', '')
        context['fecha_hasta'] = self.request.GET.get('fecha_hasta', '')
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = "app/event/event_detail.html"
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tiers_with_availability = []
        for tier in self.object.ticket_tiers.filter(is_available=True):
            tier_data = {
                'tier': tier,
                'available_quantity': tier.get_available_quantity(),
                'is_sold_out': tier.get_available_quantity() <= 0
            }
            tiers_with_availability.append(tier_data)
        context['tiers_with_availability'] = tiers_with_availability
        return context

class CommentCreateView(LoginRequiredMixin, CreateView):
    model=Comment
    form_class = CommentForm
    template_name = 'comment/comment_form.html'

    def get_success_url(self):
        return reverse_lazy('comentario_listar', kwargs={'pk': self.kwargs['pk_event']})

    def form_valid(self,form):
        comment = form.save(commit=False)
        comment.event_fk = self.kwargs.get('pk_event')
        comment.user = self.request.user
        comment.save()
        messages.success(self.request, f"El comentario '{comment.title}' fue creado con exito.")
        return super().form_valid(form)
    
class CommentUpdateView(LoginRequiredMixin,UpdateView):
    model=Comment
    form_class = CommentForm
    template_name = 'comment/comment_form.html'

    def get_success_url(self):
        return reverse_lazy('comentario_listar', kwargs={'pk': self.kwargs['pk_event']})

    def get_queryset(self):
        return Comment.objects.filter(user_fk=self.request.user)
    
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.save()
        messages.success(self.request, f"el comentario {comment.title} fue actualizado correctamente.")
        return super().form_valid(form)
    
class CommentDeleteView(LoginRequiredMixin,DeleteView):
    model=Comment
    template_name = 'comment/comment_form.html'
    
    def get_success_url(self):
        return reverse_lazy('comentario_listar', kwargs={'pk': self.kwargs['pk_event']})

    def get_queryset(self):
        return Comment.objects.filter(user_fk=self.request.user)

class CommentListView(LoginRequiredMixin,ListView):
    model=Comment
    template_name="comment/comment_list.html"
    context_object_name="comentarios"

    def get_queryset(self):
        pk=self.kwargs.get('pk')
        queryset=Comment.objects.filter(event_fk=pk).order_by("-created_at")

class CommentDetailView(LoginRequiredMixin,DetailView):
    model = Comment
    template_name = "comment/comment_detail.html"
    context_object_name = "comentario"


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

class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = "app/tickets.html"
    context_object_name = "tickets"

    def get_queryset(self):
        return Ticket.objects.filter(user_fk=self.request.user).order_by("-created_at")

    def post(self, request, *args, **kwargs):
        ticket_id = request.POST.get('ticket_id')
        reason = request.POST.get('reason')

        if not reason:
            messages.error(request, "Por favor, proporciona un motivo para el reembolso.")
            return redirect('ticket_list')

        try:
            ticket = get_object_or_404(Ticket, pk=ticket_id, user_fk=request.user)

            if RefundRequest.objects.filter(ticket_code=str(ticket.pk)).exists():
                messages.error(request, "Ya solicitaste un reembolso para este ticket.")
            else:
                RefundRequest.new(
                    user=request.user,
                    ticket_code=str(ticket.pk),
                    reason=reason
                )
                messages.success(request, "Tu solicitud de reembolso fue enviada con éxito.")
        except Exception:
            messages.error(request, "Error al procesar la solicitud de reembolso.")

        return redirect('ticket_list')

class TicketDetailView(DetailView):
    model = Ticket
    template_name = "ticket/ticket_detail.html"
    context_object_name = "ticket"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket = self.get_object()
        refund_request = RefundRequest.objects.filter(ticket_code=str(ticket.pk)).first()
        context['refund_request'] = refund_request
        return context


class TicketCreateView(LoginRequiredMixin, View):
    template_name = "ticket/ticket_purchase.html"

    def get(self, request, event_pk, tier_id, *args, **kwargs):
        ticket_tier = get_object_or_404(TicketTier, pk=tier_id)
        if not ticket_tier.is_available or ticket_tier.get_available_quantity() <= 0:
            messages.error(request, "Este tipo de entrada ya no está disponible.")
            return redirect('event_detail', pk=event_pk)

        form = TicketPurchaseForm(ticket_tier=ticket_tier)
        return render(request, self.template_name, {
            'form': form,
            'ticket_tier': ticket_tier,
            'available_quantity': ticket_tier.get_available_quantity()
        })

    def post(self, request, event_pk, tier_id, *args, **kwargs):
        ticket_tier = get_object_or_404(TicketTier, pk=tier_id)
        form = TicketPurchaseForm(request.POST, ticket_tier=ticket_tier)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            if not ticket_tier.has_available_quantity(quantity):
                available = ticket_tier.get_available_quantity()
                messages.error(request, f"Solo quedan {available} entradas disponibles para esta categoría.")
                return render(request, self.template_name, {
                    'form': form,
                    'ticket_tier': ticket_tier,
                    'available_quantity': available
                })

            try:
                ticket = Ticket.objects.create(
                    ticket_tier=ticket_tier,
                    user_fk=request.user,
                    quantity=quantity
                )
                messages.success(request, f"¡Compra de {quantity} entradas realizada con éxito!")
                return redirect('ticket_detail', pk=ticket.pk)
            except ValidationError as e:
                messages.error(request, f"Error al procesar la compra: {e}")
                return redirect('event_detail', pk=event_pk)
            except Exception:
                messages.error(request, "Error inesperado al procesar la compra.")
                return redirect('event_detail', pk=event_pk)

        return render(request, self.template_name, {
            'form': form,
            'ticket_tier': ticket_tier,
            'available_quantity': ticket_tier.get_available_quantity()
        })

@method_decorator(login_required, name='dispatch')
class UserProfileView(View):
    def get(self, request, username):
        profile_user = get_object_or_404(User, username=username)
        context = {
            'profile_user': profile_user,
        }

        if request.user == profile_user:
            context['form'] = ProfileImageForm(instance=profile_user.profile)

            tickets = Ticket.objects.filter(
                user_fk=profile_user
            ).select_related(
                'ticket_tier',
                'ticket_tier__event',
                'ticket_tier__event__venue_fk',
                'promotion_used'
            ).order_by('-created_at')

            refund_ticket_ids = RefundRequest.objects.filter(
                ticket_code__in=[str(t.pk) for t in tickets]
            ).values_list('ticket_code', flat=True)

            context['user_tickets'] = [ticket for ticket in tickets if str(ticket.pk) not in refund_ticket_ids]

            context['refund_requests'] = RefundRequest.objects.filter(
                user=profile_user
            ).order_by('-created_at')

            context['now'] = timezone.now()

        return render(request, 'users/profile.html', context)

    def post(self, request, username):
        profile_user = get_object_or_404(User, username=username)
        
        if request.user != profile_user:
            messages.error(request, "No tienes permiso para modificar este perfil.")
            return redirect('user_profile', username=username)

        action = request.POST.get('action')
        
        if action == 'request_refund':
            ticket_id = request.POST.get('ticket_id')
            reason = request.POST.get('reason')
            
            if not reason or not reason.strip():
                messages.error(request, "Por favor, proporciona un motivo para el reembolso.")
                return redirect('user_profile', username=username)
            
            try:
                ticket = get_object_or_404(Ticket, pk=ticket_id, user_fk=request.user)
                
                if ticket.ticket_tier.event.date <= timezone.now():
                    messages.error(request, "No se pueden solicitar reembolsos para eventos que ya han pasado.")
                    return redirect('user_profile', username=username)
                
                if RefundRequest.objects.filter(ticket_code=str(ticket.pk)).exists():
                    messages.error(request, "Ya existe una solicitud de reembolso para este ticket.")
                    return redirect('user_profile', username=username)
                
                success, result = RefundRequest.new(
                    user=request.user,
                    ticket_code=str(ticket.pk),
                    reason=reason.strip()
                )
                
                if success:
                    messages.success(request, "Tu solicitud de reembolso ha sido enviada con éxito. Será revisada por nuestro equipo.")
                else:
                    messages.error(request, "Error al procesar la solicitud de reembolso.")
                    
            except Exception:
                messages.error(request, "Error inesperado al procesar la solicitud de reembolso.")
                
            return redirect('user_profile', username=username)
        
        else:
            form = ProfileImageForm(request.POST, request.FILES, instance=profile_user.profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Foto de perfil actualizada.")
                return redirect('user_profile', username=username)
            messages.error(request, "Hubo un error al subir la imagen.")
            return render(request, 'users/profile.html', {
                'profile_user': profile_user,
                'form': form
            })


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'app/notificacion/notificaciones.html'
    context_object_name = 'notificaciones'

    def get_queryset(self):
        return Notification.objects.filter(users=self.request.user).order_by('-created_at')

    def post(self, request, *args, **kwargs):
        notification_id = request.POST.get('notification_id')
        if notification_id:
            notification = get_object_or_404(Notification, pk=notification_id, users=request.user)
            notification.is_read = True
            notification.save()
            messages.success(request, 'Notificación marcada como leída.')
        else:
            messages.error(request, 'ID de notificación no válido.')
        return redirect('notificaciones')

class NotificationDetailView(DetailView):
    model = Notification
    template_name = "app/notificacion/notification_detail.html"
    context_object_name = "notificacion"

class VenueListView(ListView):
    model = Venue
    template_name = 'venue/venue_list.html'
    context_object_name = 'venues'
    paginate_by = 10

class VenueDetailView(DetailView):
    model = Venue
    template_name = "venue/venue_detalle.html"
    context_object_name = "venue"

class CategoryListView(ListView):
    model = Category
    template_name = "category/category_list.html"
    context_object_name = "categories"

class CategoryDetailView(DetailView):
    model = Category
    template_name = "category/category_detail.html"
    context_object_name = "category"