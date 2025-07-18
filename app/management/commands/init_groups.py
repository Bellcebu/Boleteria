from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from app.models import Event, Category, Venue, RefundRequest, Promotion, Comment, Ticket


class Command(BaseCommand):
    help = "Inicializa grupos y permisos para Admin y Vendedor"

    def handle(self, *args, **kwargs):
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        vendedor_group, _ = Group.objects.get_or_create(name='Vendedor')

        def get_perms(model, actions):
            ct = ContentType.objects.get_for_model(model)
            return Permission.objects.filter(
                content_type=ct,
                codename__in=[f"{action}_{model._meta.model_name}" for action in actions]
            )

        admin_perms = (
            get_perms(Event, ['add', 'change', 'delete', 'view']) |
            get_perms(Category, ['add', 'change', 'delete', 'view']) |
            get_perms(Venue, ['add', 'change', 'delete', 'view']) |
            get_perms(RefundRequest, ['view'])
        )
        admin_group.permissions.set(admin_perms)

        vendedor_perms = (
            get_perms(Event, ['view']) | 
            get_perms(Category, ['view']) |  
            get_perms(Venue, ['view']) |  
            get_perms(Promotion, ['add', 'change', 'delete', 'view']) |  
            get_perms(RefundRequest, ['change', 'view']) |  
            get_perms(Comment, ['delete', 'view']) |  
            get_perms(Ticket, ['change', 'view'])
        )

        vendedor_group.permissions.set(vendedor_perms)

        self.stdout.write(self.style.SUCCESS("Grupos y permisos configurados correctamente."))
