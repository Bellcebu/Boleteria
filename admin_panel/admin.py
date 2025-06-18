from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from app.models import Event, Category

admin_group, _ = Group.objects.get_or_create(name='Admin')
vendedor_group, _ = Group.objects.get_or_create(name='Vendedor')

event_ct = ContentType.objects.get_for_model(Event)
category_ct = ContentType.objects.get_for_model(Category)

admin_permissions = Permission.objects.filter(content_type__in=[event_ct, category_ct])
admin_group.permissions.set(admin_permissions)

view_event_perm = Permission.objects.get(codename='view_event')
vendedor_group.permissions.add(view_event_perm)
