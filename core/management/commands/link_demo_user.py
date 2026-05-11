from getpass import getpass

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.models import Professional


class Command(BaseCommand):
    help = 'Crea (o actualiza) un User y lo asocia a un Professional existente vía email.'

    def add_arguments(self, parser):
        parser.add_argument('username', help='Username del nuevo user (o existente).')
        parser.add_argument('--email', required=True, help='Email del Professional a linkear.')
        parser.add_argument('--password', help='Password del user. Si se omite, se pide interactivamente.')
        parser.add_argument('--superuser', action='store_true', help='Otorga is_staff=True e is_superuser=True.')

    @transaction.atomic
    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        is_superuser = options['superuser']

        try:
            professional = Professional.objects.get(email=email)
        except Professional.DoesNotExist:
            raise CommandError(f'No existe un Professional con email {email}. Corré primero seed_demo_professional.')

        if not password:
            password = getpass('Password para el user: ')
            if not password:
                raise CommandError('La password no puede estar vacía.')

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email},
        )

        user.email = email
        user.set_password(password)
        if is_superuser:
            user.is_staff = True
            user.is_superuser = True
        user.save()

        professional.user = user
        professional.save()

        action = 'creado' if created else 'actualizado'
        suffix = ' (staff + superuser)' if is_superuser else ''
        self.stdout.write(self.style.SUCCESS(
            f'User {action}: {user.username}{suffix}  →  {professional.professional_name}'
        ))
