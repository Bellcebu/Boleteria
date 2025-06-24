from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.utils import timezone
from django.utils.timezone import now

from app.models import Event, Category, Venue, RefundRequest, TicketTier, Ticket,Comment, Notification
from app.forms import EventModelForm, CategoryModelForm, VenueModelForm, TicketModelForm, TicketTierFormSet,CommentForm,NotificationModelForm


def is_admin(user):
    return user.is_staff or user.groups.filter(name='Admin').exists()

def is_vendedor(user):
    return user.groups.filter(name='Vendedor').exists() 


class AdminHomeView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'admin_template/admin_home.html'
    
    def test_func(self):
        return is_admin(self.request.user)
    
    def get(self, request):
        context = {
            'total_events': Event.objects.count(),
            'total_categories': Category.objects.count(),
            'total_users': User.objects.count(),
            'total_venues': Venue.objects.count(),
        }
        return render(request, self.template_name, context)


class VendedorHomeView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'vendedor_template/vendedor_home.html'
    
    def test_func(self):
        return is_vendedor(self.request.user)
    
    def get(self, request):
        context = {
            'total_events': Event.objects.count(),
            'total_users': User.objects.count(),
            'pending_refunds': RefundRequest.objects.filter(approved=False).count(),
            'total_comments': Comment.objects.count(),
        }
        return render(request, self.template_name, context)


# --- Eventos CRUD ---

class AdminEventView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'admin_template/admin_event.html'
   
    def test_func(self):
        return is_admin(self.request.user) or is_vendedor(self.request.user)
   
    def get(self, request):
        if is_vendedor(request.user):
            self.template_name = 'vendedor_template/vendedor_event.html'
        else:
            self.template_name = 'admin_template/admin_event.html'   
        context = {
            'events': Event.objects.all().order_by('-created_at'),
            'categories': Category.objects.all(),
            'venues': Venue.objects.all(),
            'is_vendedor': is_vendedor(self.request.user),
        }
        return render(request, self.template_name, context)
   
    def post(self, request):
        action = request.POST.get('action')
        if action == 'create':
            if is_vendedor(request.user):
                messages.error(request, "No tienes permisos para crear eventos.")
                return redirect('admin_event')
               
            form = EventModelForm(request.POST, request.FILES)
            if form.is_valid():
                event = form.save()
                messages.success(request, f"Evento '{event.title}' creado con éxito.")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{form.fields[field].label}: {error}")
       
        elif action == 'edit':
            event_id = request.POST.get('event_id')
            event = get_object_or_404(Event, pk=event_id)
            form = EventModelForm(request.POST, request.FILES, instance=event)
            if form.is_valid():
                event = form.save()
                messages.success(request, f"Evento '{event.title}' actualizado con éxito.")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{form.fields[field].label}: {error}")
       
        elif action == 'delete':
            if is_vendedor(request.user):
                messages.error(request, "No tienes permisos para eliminar eventos.")
                return redirect('admin_event')
               
            event_id = request.POST.get('event_id')
            event = get_object_or_404(Event, pk=event_id)
            event_title = event.title
            event.delete()
            messages.success(request, f"Evento '{event_title}' eliminado con éxito.")
       
        return redirect('admin_event')

# --- Ticket CRUD ---

class AdminEventTicketsView(LoginRequiredMixin, UserPassesTestMixin, View):
   
    def test_func(self):
        return is_admin(self.request.user) or is_vendedor(self.request.user)
   
    def get(self, request, event_id):
        if is_admin(self.request.user):
            template_name = 'admin_template/admin_tickets.html'
        else:
            template_name = 'vendedor_template/vendedor_tickets.html'
   
        event = get_object_or_404(Event, id=event_id)
        tickets = TicketTier.objects.filter(event=event).order_by('price')
       
        context = {
            'event': event,
            'tickets': tickets,
        }
        return render(request, template_name, context)
   
    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        action = request.POST.get('action')
       
        if action == 'create':
            ticket = TicketTier(event=event)
            form = TicketModelForm(request.POST, instance=ticket)
            if form.is_valid():
                form.save()
                messages.success(request, f"Ticket '{ticket.name}' creado con éxito.")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{form.fields[field].label}: {error}")
       
        elif action == 'edit':
            ticket_id = request.POST.get('ticket_id')
            ticket = get_object_or_404(TicketTier, pk=ticket_id, event=event)
            form = TicketModelForm(request.POST, instance=ticket)
            if form.is_valid():
                ticket = form.save()
                messages.success(request, f"Ticket '{ticket.name}' actualizado con éxito.")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{form.fields[field].label}: {error}")
       
        elif action == 'delete':
            ticket_id = request.POST.get('ticket_id')
            ticket = get_object_or_404(TicketTier, pk=ticket_id, event=event)
           
            if ticket.sold_quantity > 0:
                messages.error(request, f"No se puede eliminar '{ticket.name}' porque ya hay {ticket.sold_quantity} entradas vendidas.")
            else:
                ticket_name = ticket.name
                ticket.delete()
                messages.success(request, f"Ticket '{ticket_name}' eliminado con éxito.")
       
        return redirect('event_tickets', event_id=event_id)

# --- Categorías CRUD ---

class AdminCategoriesView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'admin_template/admin_categories.html'
    
    def test_func(self):
        return is_admin(self.request.user)
    
    def get(self, request):
        context = {
            'categories': Category.objects.all().order_by('-created_at'),
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        action = request.POST.get('action')
        
        if action == 'create':
            form = CategoryModelForm(request.POST)
            if form.is_valid():
                category = form.save()
                messages.success(request, f"Categoría '{category.name}' creada con éxito.")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{form.fields[field].label}: {error}")
        
        elif action == 'edit':
            category_id = request.POST.get('category_id')
            category = get_object_or_404(Category, pk=category_id)
            form = CategoryModelForm(request.POST, instance=category)
            if form.is_valid():
                category = form.save()
                messages.success(request, f"Categoría '{category.name}' actualizada con éxito.")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{form.fields[field].label}: {error}")
        
        elif action == 'delete':
            category_id = request.POST.get('category_id')
            category = get_object_or_404(Category, pk=category_id)
            category_name = category.name
            category.delete()
            messages.success(request, f"Categoría '{category_name}' eliminada con éxito.")
        
        return redirect('admin_categories')

# --- Venues CRUD ---

class AdminVenueView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'admin_template/admin_venue.html'
    
    def test_func(self):
        return is_admin(self.request.user)
    
    def get(self, request):
        context = {
            'venues': Venue.objects.all().order_by('-created_at'),
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        action = request.POST.get('action')
        
        if action == 'create':
            form = VenueModelForm(request.POST)
            if form.is_valid():
                venue = form.save()
                messages.success(request, f"Lugar '{venue.name}' creado con éxito.")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{form.fields[field].label}: {error}")
        
        elif action == 'edit':
            venue_id = request.POST.get('venue_id')
            venue = get_object_or_404(Venue, pk=venue_id)
            form = VenueModelForm(request.POST, instance=venue)
            if form.is_valid():
                venue = form.save()
                messages.success(request, f"Lugar '{venue.name}' actualizado con éxito.")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{form.fields[field].label}: {error}")
        
        elif action == 'delete':
            venue_id = request.POST.get('venue_id')
            venue = get_object_or_404(Venue, pk=venue_id)
            venue_name = venue.name
            venue.delete()
            messages.success(request, f"Lugar '{venue_name}' eliminado con éxito.")
        
        return redirect('admin_venue')


# --- Refund Requests CRUD ---

class AdminRefundRequesView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return is_admin(self.request.user) or is_vendedor(self.request.user)
   
    def get(self, request):
        if is_admin(self.request.user):
            template_name = 'admin_template/admin_refund_request.html'
        else: 
            template_name = 'vendedor_template/vendedor_refund_request.html'
        
        context = {
            'pending_refunds': RefundRequest.objects.filter(
                approved=False,
                processed_by__isnull=True
            ).order_by('-created_at'),
            'processed_refunds': RefundRequest.objects.filter(
                processed_by__isnull=False
            ).order_by('-approval_date'),
        }
        return render(request, template_name, context)
    
    def post(self, request):
        action = request.POST.get('action')
        refund_id = request.POST.get('refund_id')
        
        try:
            refund = get_object_or_404(RefundRequest, pk=refund_id)
            
            if action == 'approve':
                refund.approved = True
                refund.approval_date = timezone.now().date()
                refund.processed_by = request.user
                refund.save()
                messages.success(request, f"Reembolso del ticket #{refund.ticket_code} aprobado con éxito.")
                
            elif action == 'reject':
                refund.approved = False
                refund.approval_date = timezone.now().date()
                refund.processed_by = request.user
                refund.save()
                messages.success(request, f"Reembolso del ticket #{refund.ticket_code} rechazado.")
                
        except Exception as e:
            messages.error(request, f"Error al procesar el reembolso: {str(e)}")
        
        return redirect('admin_refund_request')

# --- Roles ---

class AdminRolsView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'admin_template/admin_rols.html'
   
    def test_func(self):
        return is_admin(self.request.user)
        
    def get(self, request):
        users = User.objects.all().order_by('username')
        users_with_roles = []
        for user in users:
            if user.is_superuser:
                current_role = 'admin'
            elif user.groups.filter(name='Admin').exists():
                current_role = 'admin'
            elif user.groups.filter(name='Vendedor').exists():
                current_role = 'vendedor'
            else:
                current_role = 'usuario'
            users_with_roles.append({
                'user': user,
                'current_role': current_role,
            })
        return render(request, self.template_name, {'users_with_roles': users_with_roles})
        
    def post(self, request):
        action = request.POST.get('action')
        if action == 'assign_role':
            user_id = request.POST.get('user_id')
            role = request.POST.get('role')
            user = get_object_or_404(User, id=user_id)
            if user == request.user and role != 'admin':
                messages.error(request, "No puedes quitarte permisos de administrador a ti mismo.")
                return redirect('admin_rols')
            user.groups.clear()
            if role == 'admin':
                admin_group, _ = Group.objects.get_or_create(name='Admin')
                user.groups.add(admin_group)
                user.is_staff = True
                user.save()
                messages.success(request, f"Usuario '{user.username}' asignado como Administrador.")
            elif role == 'vendedor':
                vendedor_group, _ = Group.objects.get_or_create(name='Vendedor')
                user.groups.add(vendedor_group)
                user.is_staff = False
                user.save()
                messages.success(request, f"Usuario '{user.username}' asignado como Vendedor.")
            elif role == 'usuario':
                user.is_staff = False
                user.save()
                messages.success(request, f"Usuario '{user.username}' asignado como Usuario normal.")
        return redirect('admin_rols')
        
# List View
class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "notification/notification_list.html"
    context_object_name = "notifications"

# Create View
class NotificationCreateView(LoginRequiredMixin, CreateView):
    model = Notification
    form_class = NotificationModelForm
    template_name = "notification/notification_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Notification created successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("notification_list")

# Update View
class NotificationUpdateView(LoginRequiredMixin, UpdateView):
    model = Notification
    form_class = NotificationModelForm
    template_name = "notification/notification_form.html"

    def form_valid(self, form):
        messages.success(self.request, f"Notification '{form.instance.title}' updated.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("notification_list")

# Delete View
class NotificationDeleteView(LoginRequiredMixin, DeleteView):
    model = Notification
    template_name = "notification/notification_confirm_delete.html"

    def get_success_url(self):
        messages.success(self.request, "Notification deleted.")
        return reverse_lazy("notification_list")

# Detail View
class NotificationDetailView(LoginRequiredMixin, DetailView):
    model = Notification
    template_name = "notification/notification_detail.html"
    context_object_name = "notification"