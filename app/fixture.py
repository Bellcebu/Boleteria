from django.contrib.auth.models import User, Group, Permission

admin = Group.objects.create(name='Administradores')
vendedor = Group.objects.create(name='Vendedor')
cliente = Group.objects.create(name='Cliente')


permission = Permission.objects.get(codename='can_create_category')
admin.permissions.add(permission)

permission = Permission.objects.get(codename='can_view_refund_request')
admin.permissions.add(permission)

permission = Permission.objects.get(codename='can_update_category')
admin.permissions.add(permission)

permission = Permission.objects.get(codename='can_delete_category')
admin.permissions.add(permission)

permission = Permission.objects.get(codename='can_create_venue')
admin.permissions.add(permission)

permission = Permission.objects.get(codename='can_update_venue')
admin.permissions.add(permission)

permission = Permission.objects.get(codename='can_delete_venue')
admin.permissions.add(permission)


