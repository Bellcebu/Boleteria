from django.views.generic import TemplateView, ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse_lazy

from admin_panel.views import is_admin, is_vendedor

from .forms import (
    SignUpForm,
    CommentForm,
    RatingModelForm,
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
    Promotion,
    Venue,
    Category,
    Rating,
    Favorito,
    Notification,
)


class HomeView(TemplateView):
    template_name = 'user_template/home.html'

    def get_events_for_user(self, user):  
        if user.is_staff or user.groups.filter(name='Vendedor').exists():
            return Event.objects.all()  
        else:
            return Event.objects.filter(date__gte=timezone.now())[:8]
    
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
            
            if is_admin(user):
                return redirect('admin_home')
            elif is_vendedor(user):
                return redirect('vendedor_home')
            else:
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
    template_name = "user_template/event_list.html"
    context_object_name = "eventos"
    paginate_by = 12

    def get_queryset(self):
        queryset = Event.objects.filter(date__gte=timezone.now())

        categoria_id = self.request.GET.get('categoria')
        if categoria_id:
            queryset = queryset.filter(category=categoria_id)  
            
        return queryset.order_by('date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Category.objects.all()
        context['categoria_seleccionada'] = self.request.GET.get('categoria', '')
        return context

class EventDetailView(View):
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        tiers_with_availability = [
            {
                'tier': tier,
                'available_quantity': tier.get_available_quantity(),
                'is_sold_out': tier.get_available_quantity() <= 0
            }
            for tier in event.ticket_tiers.filter(is_available=True)
        ]
        context = {
            'event': event,
            'tiers_with_availability': tiers_with_availability,
            'is_favorito': False,
        }
        if request.user.is_authenticated:
            context['is_favorito'] = Favorito.objects.filter(
                user_fk=request.user,
                event_fk=event
            ).exists()
        return render(request, 'user_template/event_detail.html', context)

    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para realizar esta acción.")
            return redirect('login')

        favorito, created = Favorito.objects.get_or_create(user_fk=request.user, event_fk=event)
        if not created:
            favorito.delete()
            messages.info(request, "Evento removido de favoritos.")
        else:
            messages.success(request, "Evento agregado a tus favoritos.")
        
        return redirect('event_detail', pk=pk)


class EditCommentView(View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para realizar esta acción.")
            return redirect('login')
        
        comment_id = request.POST.get("comment_id")
        comment = get_object_or_404(Comment, pk=comment_id, user_fk=request.user)
        
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comentario actualizado con éxito.")
        else:
            messages.error(request, "Error al editar el comentario.")
        
        return redirect('event_detail', pk=pk)


class DeleteCommentView(View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para realizar esta acción.")
            return redirect('login')
        
        comment_id = request.POST.get("comment_id")
        comment = get_object_or_404(Comment, pk=comment_id, user_fk=request.user)
        
        comment.delete()
        messages.success(request, "Comentario eliminado con éxito.")
        
        return redirect('event_detail', pk=pk)
    
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def get_success_url(self):    
        return reverse_lazy('event_detail', kwargs={'pk': self.kwargs['pk_event']})

    def form_valid(self, form):
        event_pk = self.kwargs.get('pk_event')
        event = get_object_or_404(Event, pk=event_pk)
        
        comment = form.save(commit=False)
        comment.event_fk = event 
        comment.user_fk = self.request.user 
        comment.save()
        
        messages.success(self.request, f"El comentario '{comment.title}' fue creado con éxito.")
        return super().form_valid(form)

class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = "user_template/tickets.html"
    context_object_name = "tickets"

    def get_queryset(self):
        return Ticket.objects.filter(user_fk=self.request.user).order_by("-created_at")

    def post(self, request, *args, **kwargs):
        form = RefundRequestForm(request.POST)
        if form.is_valid():
            ticket_code = form.cleaned_data['ticket_code']
            reason = form.cleaned_data['reason']

            try:
                ticket = get_object_or_404(Ticket, pk=ticket_code, user_fk=request.user)
            except:
                messages.error(request, "Ticket no encontrado o no te pertenece.")
                return redirect('ticket_list')

            if RefundRequest.objects.filter(ticket_code=str(ticket.pk)).exists():
                messages.error(request, "Ya solicitaste un reembolso para este ticket.")
            else:
                RefundRequest.objects.create(
                    user=request.user,
                    ticket_code=str(ticket.pk),
                    reason=reason
                )
                messages.success(request, "Tu solicitud de reembolso fue enviada con éxito.")
        else:
            for field, errors in form.errors.items():
                messages.error(request, f"{form.fields[field].label}: {errors[0]}")
        return redirect('ticket_list')


class TicketDetailView(DetailView):
    model = Ticket
    template_name = "user_template/ticket_detail.html"
    context_object_name = "ticket"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket = self.get_object()
        refund_request = RefundRequest.objects.filter(ticket_code=str(ticket.pk)).first()
        context['refund_request'] = refund_request
        return context


class TicketPurchaseView(LoginRequiredMixin, View):
    template_name = 'user_template/ticket_purchase.html'
    
    def get(self, request, event_id, tier_id):
        ticket_tier = get_object_or_404(TicketTier, pk=tier_id, event__pk=event_id)
        available_quantity = ticket_tier.available_quantity
        
        if available_quantity <= 0:
            messages.error(request, "No hay entradas disponibles.")
            return redirect('event_detail', pk=event_id)
        
        valid_promotions = Promotion.objects.filter(
            event=ticket_tier.event,
            is_active=True
        )
        
        context = {
            'ticket_tier': ticket_tier,
            'available_quantity': available_quantity,
            'valid_promotions': valid_promotions,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, event_id, tier_id):
        ticket_tier = get_object_or_404(TicketTier, pk=tier_id, event__pk=event_id)
        quantity = int(request.POST.get('quantity', 1))
        promotion_code = request.POST.get('promotion_code', '').strip().upper()
        
        available_quantity = ticket_tier.available_quantity
        if quantity > available_quantity:
            messages.error(request, "No hay suficientes entradas disponibles.")
            return redirect('ticket_purchase', event_id=event_id, tier_id=tier_id)
        
        original_price = quantity * ticket_tier.price
        final_price = original_price
        promotion_used = None
        
        if promotion_code:
            try:
                promotion = Promotion.objects.get(
                    event=ticket_tier.event,
                    code=promotion_code,
                    is_active=True
                )
                
                if promotion.is_valid_now:
                    discount_amount = (original_price * promotion.discount_percentage) / 100
                    final_price = original_price - discount_amount
                    promotion_used = promotion
                else:
                    messages.error(request, "El código promocional ha expirado.")
                    return redirect('ticket_purchase', event_id=event_id, tier_id=tier_id)
                
            except Promotion.DoesNotExist:
                messages.error(request, "Código promocional no válido.")
                return redirect('ticket_purchase', event_id=event_id, tier_id=tier_id)
        
        ticket = Ticket.objects.create(
            ticket_tier=ticket_tier,
            user_fk=request.user,
            quantity=quantity,
            promotion_used=promotion_used
        )
        
        messages.success(request, f"Compra realizada. Total: ${ticket.final_price:.2f}")
        return redirect('event_detail', pk=event_id)


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

        return render(request, 'user_template/profile.html', context)

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
                
                RefundRequest.objects.create(
                    user=request.user,
                    ticket_code=str(ticket.pk),
                    reason=reason.strip()
                )
                messages.success(request, "Tu solicitud de reembolso ha sido enviada con éxito. Será revisada por nuestro equipo.")
                    
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
            return render(request, 'user_template/profile.html', {
                'profile_user': profile_user,
                'form': form
            })

class RatingCreateView(LoginRequiredMixin, CreateView):
    model = Rating
    form_class = RatingModelForm
    template_name = "rating/rating_form.html"

    def form_valid(self, form):
        event = get_object_or_404(Event, pk=self.kwargs.get('pk_event'))
        form.instance.user_fk = self.request.user
        form.instance.event_fk = event
        messages.success(self.request, "Tu calificación fue enviada.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("event_detail", kwargs={'pk': self.kwargs.get('pk_event')})


class RatingUpdateView(LoginRequiredMixin, UpdateView):
    model = Rating
    form_class = RatingModelForm
    template_name = "rating/rating_form.html"

    def get_queryset(self):
        return Rating.objects.filter(user_fk=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Tu calificación fue actualizada.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("event_detail", kwargs={'pk': self.object.event_fk.pk})


class RatingDeleteView(LoginRequiredMixin, DeleteView):
    model = Rating
    template_name = "rating/rating_confirm_delete.html"

    def get_queryset(self):
        return Rating.objects.filter(user_fk=self.request.user)

    def get_success_url(self):
        return reverse_lazy("event_detail", kwargs={'pk': self.object.event_fk.pk})
    
class FavoriteListView(LoginRequiredMixin, ListView):
    model = Favorito
    template_name = "user_template/favorite.html"
    context_object_name = "favoritos"
    paginate_by = 12

    def get_queryset(self):
        return Favorito.objects.filter(
            user_fk=self.request.user,
            event_fk__date__gte=timezone.now()
        ).select_related('event_fk', 'event_fk__venue_fk').prefetch_related('event_fk__category')

    def post(self, request, *args, **kwargs):
        event_id = request.POST.get('event_id')
        if event_id:
            try:
                favorito = Favorito.objects.get(
                    user_fk=request.user,
                    event_fk_id=event_id
                )
                favorito.delete()
                messages.success(request, "Evento removido de favoritos.")
            except Favorito.DoesNotExist:
                messages.error(request, "El evento no estaba en favoritos.")
        
        return redirect('favoritos')
    

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    context_object_name = "notificaciones"
    
    def get_queryset(self):
        return self.request.user.notificaciones.all().order_by("-created_at")
    
class NotificationMarkReadView(LoginRequiredMixin, View):
    def post(self, request, notification_id):
        try:
            notification = get_object_or_404(
                Notification, 
                id=notification_id, 
                users=request.user
            )
            notification.is_read = True
            notification.save()
            messages.success(request, "Notificación marcada como leída.")
        except Exception as e:
            messages.error(request, "Error al marcar notificación como leída.")

        return redirect(request.META.get('HTTP_REFERER', 'home'))
    
class NotificationDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        try:
            notification = get_object_or_404(Notification, pk=pk)

            if not notification.users.filter(id=request.user.id).exists():
                messages.error(request, f"No tienes acceso a esta notificación. Usuario: {request.user.username}")
                return redirect('home')

            if not notification.is_read:
                notification.is_read = True
                notification.save()
            
            context = {'notificacion': notification}
            return render(request, 'user_template/notification_detail.html', context)
            
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('home')