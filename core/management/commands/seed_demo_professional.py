from datetime import time

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import (
    LandingCredential,
    LandingService,
    LandingStat,
    LandingTestimonial,
    Professional,
)


PROFESSIONAL_DATA = {
    'professional_name': 'Lic. Florencia Méndez',
    'specialty': 'Psicóloga Clínica · Adultos y adolescentes',
    'phone': '+54 11 4567 8901',
    'address': 'Av. Santa Fe 2480, piso 3 "B", CABA',
    'tagline': 'Acompañamiento psicológico cercano, profesional y a tu ritmo.',
    'attention_mode': 'Presencial y online',
    'accepts_insurance': True,
    'accepts_private': True,
    'bio': (
        'Soy psicóloga clínica con más de doce años de experiencia trabajando '
        'con adultos y adolescentes. Mi enfoque parte de la terapia '
        'cognitivo-conductual, integrando herramientas de mindfulness y '
        'terapias contextuales según lo que cada persona necesita. Atiendo de '
        'forma presencial en mi consultorio en Recoleta y online a quienes '
        'prefieren mantener el espacio terapéutico desde su casa. Trabajo con '
        'ansiedad, depresión, autoestima, vínculos, duelos y crisis vitales.'
    ),
    'mission': (
        'Cada proceso terapéutico es único. Mi compromiso es escuchar sin '
        'apurar, respetar tu ritmo y construir juntos un espacio donde puedas '
        'pensarte, entenderte y avanzar. No vengo con respuestas armadas: '
        'vengo a acompañar las tuyas.'
    ),
    'common_reasons': 'Ansiedad, Depresión, Autoestima, Estrés laboral, Vínculos, Duelo, Crisis vitales',
    'theme_primary': '#0047ab',
    'working_days': 'lunes,martes,miercoles,jueves,viernes',
    'start_time': time(9, 0),
    'end_time': time(19, 0),
    'appointment_duration_minutes': 50,
}

STATS = [
    ('12+', 'Años de experiencia'),
    ('800+', 'Pacientes acompañados'),
    ('95%', 'Satisfacción reportada'),
    ('4.9', 'Calificación promedio'),
]

CREDENTIALS = [
    ('school', 'Lic. en Psicología', 'Universidad de Buenos Aires (UBA), 2013'),
    ('workspace_premium', 'Especialista en Terapia Cognitivo-Conductual', 'APBA — Asociación Argentina de Terapia Cognitiva'),
    ('verified', 'Matrícula Nacional N° 45.892', 'Habilitada en CABA y Provincia de Buenos Aires'),
    ('menu_book', 'Posgrado en Trastornos de Ansiedad', 'Universidad Favaloro, 2018'),
]

SERVICES = [
    ('psychology', 'Terapia individual', 'Sesiones semanales para adultos y adolescentes. Trabajo enfocado en ansiedad, autoestima, vínculos y desarrollo personal. Duración 50 minutos.'),
    ('video_chat', 'Sesiones online', 'Misma calidad terapéutica desde donde estés. Plataforma segura y privada, sin necesidad de descargar nada.'),
    ('groups', 'Terapia de pareja', 'Espacio para parejas que quieren reordenar su comunicación, expectativas y formas de vincularse. Duración 75 minutos.'),
    ('medical_services', 'Primera entrevista', 'Encuentro inicial sin costo para conocernos, definir objetivos y evaluar si soy la profesional adecuada para vos.'),
]

TESTIMONIALS = [
    ('Florencia me ayudó a atravesar un momento muy difícil. Su forma de escuchar y guiar el proceso fue clave para volver a sentirme yo misma.', 'Carolina M.', 'Paciente desde 2023', 5),
    ('El primer espacio en el que realmente sentí que podía hablar sin ser juzgada. La recomiendo cien por ciento.', 'Sofía R.', 'Terapia individual', 5),
    ('Empecé a hacer terapia online por practicidad y la calidad del vínculo es la misma que en presencial. Excelente profesional.', 'Lucía P.', 'Modalidad online', 5),
    ('Trabajamos varios temas a lo largo de un año. Hoy tengo herramientas que uso todos los días. Una persona genuina y comprometida.', 'Andrea T.', 'Paciente desde 2022', 5),
]


class Command(BaseCommand):
    help = 'Crea (o actualiza) una profesional demo (Lic. Florencia Méndez) con stats, credenciales, servicios y testimonios.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            default='contacto@florenciamendez.com.ar',
            help='Email de la profesional demo (clave de deduplicación).',
        )
        parser.add_argument(
            '--reset-children',
            action='store_true',
            help='Borra stats/credenciales/servicios/testimonios previos antes de cargar los nuevos.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        email = options['email']

        professional, created = Professional.objects.update_or_create(
            email=email,
            defaults=PROFESSIONAL_DATA,
        )
        action = 'creada' if created else 'actualizada'
        self.stdout.write(self.style.SUCCESS(f'Profesional {action}: {professional.professional_name} ({email})'))
        self.stdout.write(f'  slug: {professional.slug}')

        if options['reset_children']:
            LandingStat.objects.filter(professional=professional).delete()
            LandingCredential.objects.filter(professional=professional).delete()
            LandingService.objects.filter(professional=professional).delete()
            LandingTestimonial.objects.filter(professional=professional).delete()
            self.stdout.write(self.style.WARNING('  hijos previos eliminados'))

        for order, (value, label) in enumerate(STATS):
            LandingStat.objects.update_or_create(
                professional=professional, label=label,
                defaults={'value': value, 'order': order},
            )

        for order, (icon, title, subtitle) in enumerate(CREDENTIALS):
            LandingCredential.objects.update_or_create(
                professional=professional, title=title,
                defaults={'icon': icon, 'subtitle': subtitle, 'order': order},
            )

        for order, (icon, title, description) in enumerate(SERVICES):
            LandingService.objects.update_or_create(
                professional=professional, title=title,
                defaults={'icon': icon, 'description': description, 'order': order},
            )

        for order, (quote, author_name, author_meta, rating) in enumerate(TESTIMONIALS):
            LandingTestimonial.objects.update_or_create(
                professional=professional, author_name=author_name,
                defaults={'quote': quote, 'author_meta': author_meta, 'rating': rating, 'order': order},
            )

        self.stdout.write(self.style.SUCCESS(f'  {len(STATS)} stats · {len(CREDENTIALS)} credenciales · {len(SERVICES)} servicios · {len(TESTIMONIALS)} testimonios'))
        self.stdout.write(self.style.SUCCESS(f'Listo. Landing pública: /p/{professional.slug}/'))
