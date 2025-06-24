from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.utils.timezone import now

from app.models import Event, Category, Venue, RefundRequest, TicketTier, Ticket,Comment, Notification
from app.forms import EventModelForm, CategoryModelForm, VenueModelForm, TicketModelForm, TicketTierFormSet,CommentForm,NotificationModelForm


def is_admin(user):
    return user.is_staff or user.groups.filter(name='Admin').exists()

def is_vendedor(user):
    return user.groups.filter(name='Vendedor').exists() 


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    context = {
        'total_events': Event.objects.count(),
        'total_categories': Category.objects.count(),
        'total_users': User.objects.count(),
    }
    return render(request, 'admin_dashboard.html', context)


# --- Eventos CRUD ---

class EventCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Event
    form_class = EventModelForm
    template_name = 'app/event/event_create.html'
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return is_admin(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['formset'] = TicketTierFormSet(self.request.POST)
        else:
            context['formset'] = TicketTierFormSet()
        return context

    def form_valid(self, form):
        self.object = form.save()
        formset = TicketTierFormSet(self.request.POST, instance=self.object)
        if formset.is_valid():
            formset.save()
            messages.success(self.request, f"El evento '{self.object.title}' fue creado con éxito.")
            return redirect(self.success_url)
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )


class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventModelForm
    template_name = 'app/event/event_edit.html'
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return is_admin(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['form'] = self.form_class(self.request.POST, self.request.FILES, instance=self.object)
            context['formset'] = TicketTierFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['form'] = self.form_class(instance=self.object)
            context['formset'] = TicketTierFormSet(instance=self.object)
        context['event'] = self.object
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, request.FILES, instance=self.object)
        formset = TicketTierFormSet(request.POST, request.FILES, instance=self.object)
        
        if form.is_valid():
            self.object = form.save()
            print("Imagen guardada en modelo:", self.object.image)
            if formset.is_valid():
                formset.instance = self.object
                formset.save()
            else:
                print("No se guardó el formset (errors):", formset.errors)

            messages.success(request, f"El evento '{self.object.title}' fue editado con éxito.")
            return redirect(self.success_url)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))



class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'app/event/event_confirm_delete.html'
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return is_admin(self.request.user)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, f"El evento '{obj.title}' fue eliminado.")
        return super().delete(request, *args, **kwargs)


# --- Categorías CRUD ---

class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Category
    form_class = CategoryModelForm
    template_name = 'category/category_create.html'
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return is_admin(self.request.user)

    def form_valid(self, form):
        messages.success(self.request, f"La categoría '{form.instance.name}' fue creada con éxito.")
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    form_class = CategoryModelForm
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return is_admin(self.request.user)

    def form_valid(self, form):
        messages.success(self.request, f"La categoría '{form.instance.name}' fue editada con éxito.")
        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'category/category_confirm_delete.html'
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return is_admin(self.request.user)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, f"La categoría '{obj.name}' fue eliminada.")
        return super().delete(request, *args, **kwargs)


# --- Venues CRUD ---

class VenueCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Venue
    form_class = VenueModelForm
    template_name = 'venue/venue_form.html'
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return is_admin(self.request.user)

    def form_valid(self, form):
        messages.success(self.request, f"El venue '{form.instance.name}' fue creado con éxito.")
        return super().form_valid(form)


class VenueUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Venue
    form_class = VenueModelForm
    template_name = 'venue/venue_form.html'
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return is_admin(self.request.user)

    def form_valid(self, form):
        messages.success(self.request, f"El venue '{form.instance.name}' fue editado con éxito.")
        return super().form_valid(form)


class VenueDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Venue
    template_name = 'venue/venue_confirm_delete.html'
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return is_admin(self.request.user)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, f"El venue '{obj.name}' fue eliminado.")
        return super().delete(request, *args, **kwargs)


# --- Refund Requests CRUD ---

class RefundRequestListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = RefundRequest
    template_name = 'refund_request/refund_request_list_admin.html'
    context_object_name = 'refund_requests'
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return is_admin(self.request.user)

    def get_queryset(self):
        return RefundRequest.objects.all().order_by('-created_at')


# --- Roles ---

@login_required
@user_passes_test(is_admin)
def user_roles_list(request):
    users = User.objects.all().order_by('username')
    return render(request, 'user_roles.html', {'users': users})


@login_required
@user_passes_test(is_admin)
def assign_role(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        role = request.POST.get('role')
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
        return redirect('user_roles')
    current_role = 'usuario'
    if user.is_staff and user.groups.filter(name='Admin').exists():
        current_role = 'admin'
    elif user.groups.filter(name='Vendedor').exists():
        current_role = 'vendedor'
    return render(request, 'assign_role.html', {'user': user, 'current_role': current_role})

    

    

class ApproveRefundView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        ticket_code = request.POST.get("ticket_code")
        refund = RefundRequest.objects.filter(ticket_code=ticket_code, approved=False).first()
        if refund:
            refund.approved = True
            refund.approval_date = now().date()
            refund.save()
            messages.success(request, f"Reembolso aprobado para ticket {ticket_code}")
        else:
            messages.error(request, "Solicitud no encontrada o ya aprobada.")
        return redirect("refund-requests")
    
class RefundRequestListView(LoginRequiredMixin, ListView):
    template_name = "refund_requests.html"
    context_object_name = "refunds"

    def get_queryset(self):
        return RefundRequest.objects.filter(approved=False)
    
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

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