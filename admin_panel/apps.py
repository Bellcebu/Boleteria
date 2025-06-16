from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AdminPanelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_panel'

    def ready(self):
        post_migrate.connect(create_admin_group, sender=self)

def create_admin_group(sender, **kwargs):
    from django.contrib.auth.models import Group
    Group.objects.get_or_create(name='Admin')
