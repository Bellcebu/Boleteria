from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils import timezone

from app.models import Event, Category, Venue, RefundRequest, TicketTier, Ticket, Comment, Notification, Promotion
from app.forms import EventModelForm, CategoryModelForm, VenueModelForm, TicketModelForm, NotificationModelForm


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
                return redirect('event')
               
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
                return redirect('event')
               
            event_id = request.POST.get('event_id')
            event = get_object_or_404(Event, pk=event_id)
            event_title = event.title
            event.delete()
            messages.success(request, f"Evento '{event_title}' eliminado con éxito.")
       
        return redirect('event')


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
        
        return redirect('categories')


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
        
        return redirect('venue')


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
        
        return redirect('refund_request')


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
                return redirect('rols')
                
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
        return redirect('rols')


# --- Comments ---    
class AdminCommentsView(LoginRequiredMixin, UserPassesTestMixin, View):
    
    def test_func(self):
        return is_admin(self.request.user) or is_vendedor(self.request.user)
    
    def get(self, request):
        if is_admin(self.request.user):
            template_name = 'admin_template/admin_comments.html'
        else:
            template_name = 'vendedor_template/vendedor_comments.html'
        
        comments = Comment.objects.all().select_related(
            'user_fk', 'event_fk'
        ).order_by('-created_at')
        
        events = Event.objects.all().order_by('title')
        
        context = {
            'comments': comments,
            'events': events,
        }
        return render(request, template_name, context)
    
    def post(self, request):
        action = request.POST.get('action')
        
        if action == 'delete':
            comment_id = request.POST.get('comment_id')
            try:
                comment = get_object_or_404(Comment, pk=comment_id)
                comment_title = comment.title
                comment.delete()
                messages.success(request, f"Comentario '{comment_title}' eliminado con éxito.")
            except Exception as e:
                messages.error(request, f"Error al eliminar el comentario: {str(e)}")
        
        return redirect('comments')


# --- Promotions ---    
class AdminPromotionsView(LoginRequiredMixin, UserPassesTestMixin, View):
    
    def test_func(self):
        return is_admin(self.request.user) or is_vendedor(self.request.user)
    
    def get(self, request):
        if is_admin(self.request.user):
            template_name = 'admin_template/admin_promotions.html'
        else:
            template_name = 'vendedor_template/vendedor_promotions.html'
        
        promotions = Promotion.objects.all().select_related('event', 'created_by').order_by('-created_at')
        events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
        
        context = {
            'promotions': promotions,
            'events': events,
            'now': timezone.now(),
        }
        return render(request, template_name, context)
    
    def post(self, request):
        action = request.POST.get('action')
        
        if action == 'create':
            form_data = {
                'code': request.POST.get('code'),
                'discount_percentage': request.POST.get('discount_percentage'),
                'start_date': request.POST.get('start_date'),
                'end_date': request.POST.get('end_date'),
                'max_uses': request.POST.get('max_uses'),
            }
            
            try:
                event = get_object_or_404(Event, pk=request.POST.get('event'))
                promotion = Promotion.objects.create(
                    event=event,
                    code=form_data['code'].upper(),
                    discount_percentage=form_data['discount_percentage'],
                    start_date=form_data['start_date'],
                    end_date=form_data['end_date'],
                    max_uses=form_data['max_uses'],
                    is_active=request.POST.get('is_active') == 'on',
                    created_by=request.user
                )
                messages.success(request, f"Promoción '{promotion.code}' creada con éxito.")
            except Exception as e:
                messages.error(request, f"Error al crear la promoción: {str(e)}")
        
        elif action == 'edit':
            promotion_id = request.POST.get('promotion_id')
            try:
                promotion = get_object_or_404(Promotion, pk=promotion_id)
                event = get_object_or_404(Event, pk=request.POST.get('event'))
                
                promotion.event = event
                promotion.code = request.POST.get('code').upper()
                promotion.discount_percentage = request.POST.get('discount_percentage')
                promotion.start_date = request.POST.get('start_date')
                promotion.end_date = request.POST.get('end_date')
                promotion.max_uses = request.POST.get('max_uses')
                promotion.is_active = request.POST.get('is_active') == 'on'
                promotion.save()
                
                messages.success(request, f"Promoción '{promotion.code}' actualizada con éxito.")
            except Exception as e:
                messages.error(request, f"Error al actualizar la promoción: {str(e)}")
        
        elif action == 'delete':
            promotion_id = request.POST.get('promotion_id')
            try:
                promotion = get_object_or_404(Promotion, pk=promotion_id)
                promotion_code = promotion.code
                promotion.delete()
                messages.success(request, f"Promoción '{promotion_code}' eliminada con éxito.")
            except Exception as e:
                messages.error(request, f"Error al eliminar la promoción: {str(e)}")
        
        return redirect('promotions')


# --- Notificaciones CRUD ---
class NotificationListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Notification
    template_name = "notification/notification_list.html"
    context_object_name = "notifications"
    
    def test_func(self):
        return is_admin(self.request.user)


class NotificationCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Notification
    form_class = NotificationModelForm
    template_name = "notification/notification_form.html"
    
    def test_func(self):
        return is_admin(self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Notificación creada exitosamente.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("notification_list")


class NotificationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Notification
    form_class = NotificationModelForm
    template_name = "notification/notification_form.html"
    
    def test_func(self):
        return is_admin(self.request.user)

    def form_valid(self, form):
        messages.success(self.request, f"Notificación '{form.instance.title}' actualizada.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("notification_list")


class NotificationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Notification
    template_name = "notification/notification_confirm_delete.html"
    
    def test_func(self):
        return is_admin(self.request.user)

    def get_success_url(self):
        messages.success(self.request, "Notificación eliminada.")
        return reverse_lazy("notification_list")


class NotificationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Notification
    template_name = "notification/notification_detail.html"
    context_object_name = "notification"
    
    def test_func(self):
        return is_admin(self.request.user)