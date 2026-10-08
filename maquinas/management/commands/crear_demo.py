from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

USUARIOS = [
    ('operario1', 'Operario'),
    ('operario2', 'Operario'),
    ('supervisor', 'Supervisor'),
    ('jefe', 'Jefe'),
]

CLAVE = 'Demo12345'


class Command(BaseCommand):
    help = 'Crea los grupos y usuarios de demostración'

    def handle(self, *args, **options):
        for username, rol in USUARIOS:
            grupo, _ = Group.objects.get_or_create(name=rol)
            usuario, _ = User.objects.get_or_create(username=username)
            usuario.set_password(CLAVE)
            usuario.save()
            usuario.groups.set([grupo])
            self.stdout.write(f'Usuario {username} creado con rol {rol}')
