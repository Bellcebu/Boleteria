from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Elimina un superusuario por su username"

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username del superusuario a eliminar')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        try:
            user = User.objects.get(username=username, is_superuser=True)
            user.delete()
            self.stdout.write(self.style.SUCCESS(f"Superusuario '{username}' eliminado correctamente."))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"No existe un superusuario con username '{username}'."))
