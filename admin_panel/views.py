from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from app.models import Event, Category
from app.forms import EventModelForm, CategoryModelForm


def is_admin(user):
    """Verifica si el usuario es admin (staff o pertenece al grupo Admin)"""
    return user.is_staff or user.groups.filter(name='Admin').exists()


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Dashboard principal del administrador"""
    context = {
        'total_events': Event.objects.count(),
        'total_categories': Category.objects.count(),
        'total_users': User.objects.count(),
    }
    return render(request, 'admin_dashboard.html', context)


# ===== CREAR EVENTO =====
class AdminEventCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Event
    form_class = EventModelForm
    template_name = 'app/event/event_create.html'
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return is_admin(self.request.user)

    def form_valid(self, form):
        messages.success(self.request, f"El evento '{form.instance.title}' fue creado con éxito.")
        return super().form_valid(form)


# ===== CREAR CATEGORÍA =====
class AdminCategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Category
    form_class = CategoryModelForm
    template_name = 'category/category_create.html'
    success_url = reverse_lazy('admin_dashboard')

    def test_func(self):
        return is_admin(self.request.user)

    def form_valid(self, form):
        messages.success(self.request, f"La categoría '{form.instance.name}' fue creada con éxito.")
        return super().form_valid(form)


# ===== GESTIÓN DE ROLES =====
@login_required
@user_passes_test(is_admin)
def user_roles_list(request):
    """Lista todos los usuarios para gestionar roles"""
    users = User.objects.all().order_by('username')
    return render(request, 'user_roles.html', {'users': users})


@login_required
@user_passes_test(is_admin)
def assign_role(request, user_id):
    """Asigna o modifica el rol de un usuario"""
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        role = request.POST.get('role')
        
        # Remover todos los grupos actuales
        user.groups.clear()
        
        # Asignar nuevo rol
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
        
        return redirect('admin_user_roles')
    
    # Obtener rol actual
    current_role = 'usuario'  # por defecto
    if user.is_staff and user.groups.filter(name='Admin').exists():
        current_role = 'admin'
    elif user.groups.filter(name='Vendedor').exists():
        current_role = 'vendedor'
    
    context = {
        'user': user,
        'current_role': current_role,
    }
    return render(request, 'assign_role.html', context)