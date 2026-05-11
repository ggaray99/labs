import uuid
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils.text import slugify

HEX_COLOR_VALIDATOR = RegexValidator(r'^#(?:[0-9a-fA-F]{3}){1,2}$', 'Color en formato hex. Ej: #0047ab')


# Brand book v1.0 — verticales opt-in y sus tints
VERTICAL_CHOICES = [
    ('salud',     'Salud'),
    ('legal',     'Legal'),
    ('contable',  'Contable / financiero'),
    ('coaching',  'Coaching / consultoría'),
    ('creativos', 'Servicios creativos y técnicos'),
    ('bienestar', 'Bienestar'),
]

VERTICAL_TINTS = {
    'salud':     '#5BB89A',   # Mint sereno
    'legal':     '#3D4F8F',   # Indigo profundo
    'contable':  '#8C7344',   # Bronce mate
    'coaching':  '#D88061',   # Coral cálido
    'creativos': '#7D5E94',   # Plum editorial
    'bienestar': '#8A9F7E',   # Sage tierra
}

CURRENCY_CHOICES = [
    ('ARS', 'ARS — Pesos argentinos'),
    ('USD', 'USD — Dólares'),
]


class Professional(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='professional', null=True)
    professional_name = models.CharField('Nombre completo', max_length=255)
    specialty = models.CharField('Especialidad', max_length=255)
    vertical = models.CharField('Vertical', max_length=20, choices=VERTICAL_CHOICES, blank=True, default='',
                                help_text='Categoría de servicio. Si se selecciona, define el tint de acento de la landing y la OG image.')
    email = models.EmailField('Email', unique=True)
    phone = models.CharField('Teléfono', max_length=50, blank=True)
    address = models.CharField('Dirección', max_length=255, blank=True)
    bio = models.TextField('Descripción profesional', blank=True)
    tagline = models.CharField('Frase de valor', max_length=255, blank=True)
    attention_mode = models.CharField('Modalidad de atención', max_length=100, blank=True, help_text='Ej: Presencial, Online, Presencial y online')
    accepts_insurance = models.BooleanField('Acepta obra social', default=False)
    accepts_private = models.BooleanField('Acepta particular', default=True)
    profile_image = models.ImageField('Foto de perfil', upload_to='professionals/', blank=True, null=True)
    common_reasons = models.TextField('Motivos frecuentes de consulta', blank=True, help_text='Separados por coma. Ej: Ansiedad, Estrés, Autoestima')
    mission = models.TextField('Misión / Filosofía', blank=True, help_text='Frase destacada que aparece en la landing como tarjeta azul.')
    theme_primary = models.CharField('Color principal', max_length=7, default='#0047ab', validators=[HEX_COLOR_VALIDATOR],
                                     help_text='Color de CTAs, links y tarjeta de misión. Si dejás vertical seleccionada y este campo en cobalto (#0047ab), el accent toma el tint del vertical.')
    show_stats = models.BooleanField('Mostrar estadísticas', default=True)
    show_credentials = models.BooleanField('Mostrar credenciales', default=True)
    show_mission = models.BooleanField('Mostrar misión', default=True)
    show_services = models.BooleanField('Mostrar servicios', default=True)
    show_testimonials = models.BooleanField('Mostrar testimonios', default=True)
    show_contact = models.BooleanField('Mostrar sección de contacto', default=True)
    show_map = models.BooleanField('Mostrar mapa de ubicación', default=True,
                                   help_text='Solo se renderiza si además hay una dirección cargada.')
    currency = models.CharField('Moneda', max_length=3, choices=CURRENCY_CHOICES, default='ARS',
                                help_text='Moneda en la que mostrás los precios de tus servicios.')
    slug = models.SlugField(unique=True, max_length=255)
    working_days = models.CharField('Días de atención', max_length=255, help_text='Ej: lunes,martes,miercoles')
    start_time = models.TimeField('Hora de inicio')
    end_time = models.TimeField('Hora de fin')
    appointment_duration_minutes = models.IntegerField('Duración del turno (min)', default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profesional'
        verbose_name_plural = 'Profesionales'

    def __str__(self):
        return f'{self.professional_name} - {self.specialty}'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.professional_name)
            slug = base_slug
            counter = 2
            while Professional.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_working_days_list(self):
        return [d.strip().lower() for d in self.working_days.split(',') if d.strip()]

    def get_common_reasons_list(self):
        if not self.common_reasons:
            return []
        return [r.strip() for r in self.common_reasons.split(',') if r.strip()]

    @property
    def vertical_tint(self):
        """Hex del tint correspondiente a la vertical, o None si no hay vertical."""
        return VERTICAL_TINTS.get(self.vertical) if self.vertical else None

    @property
    def supports_online(self):
        """True if the pro's attention_mode mentions 'online'."""
        return 'online' in (self.attention_mode or '').lower()

    @property
    def supports_presencial(self):
        """True if the pro accepts in-person (or hasn't configured the field)."""
        attention = (self.attention_mode or '').lower()
        return 'presencial' in attention or not attention

    @property
    def both_modes(self):
        """True when the pro accepts both formats and the patient must choose."""
        return self.supports_online and self.supports_presencial

    @property
    def accent_color(self):
        """Color de acento para la landing pública.

        El tint del vertical gana cuando está definido y el profesional dejó
        theme_primary en el default (#0047ab). Si customizó theme_primary,
        ese tiene prioridad. Si no hay vertical, cae a theme_primary.
        """
        if self.vertical_tint and (self.theme_primary or '').lower() == '#0047ab':
            return self.vertical_tint
        return self.theme_primary or '#0047ab'


class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='patients')
    first_name = models.CharField('Nombre', max_length=255)
    last_name = models.CharField('Apellido', max_length=255)
    phone = models.CharField('Teléfono', max_length=50)
    email = models.EmailField('Email', blank=True)
    address = models.CharField('Dirección', max_length=255, blank=True)
    health_insurance = models.CharField('Obra social', max_length=255, blank=True)
    health_insurance_plan = models.CharField('Plan', max_length=255, blank=True)
    health_insurance_number = models.CharField('Nro. afiliado', max_length=255, blank=True)
    clinical_notes = models.TextField('Notas clínicas', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        unique_together = ['professional', 'phone']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class LandingStat(models.Model):
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='landing_stats')
    value = models.CharField('Valor', max_length=50, help_text='Ej: 15+, 10k+, 4.9, 24')
    label = models.CharField('Etiqueta', max_length=100, help_text='Ej: Años de experiencia')
    order = models.PositiveIntegerField('Orden', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Estadística de landing'
        verbose_name_plural = 'Landing — Estadísticas'

    def __str__(self):
        return f'{self.value} {self.label}'


class LandingCredential(models.Model):
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='landing_credentials')
    icon = models.CharField('Icono Material', max_length=50, default='workspace_premium',
                            help_text='Nombre de Material Symbol. Ej: school, workspace_premium, clinical_notes, verified')
    title = models.CharField('Título', max_length=200)
    subtitle = models.CharField('Institución / detalle', max_length=255, blank=True)
    order = models.PositiveIntegerField('Orden', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Credencial'
        verbose_name_plural = 'Landing — Credenciales'

    def __str__(self):
        return self.title


class LandingService(models.Model):
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='landing_services')
    icon = models.CharField('Icono Material', max_length=50, default='medical_services',
                            help_text='Nombre de Material Symbol. Ej: monitor_heart, medical_services, video_chat')
    title = models.CharField('Título', max_length=100)
    description = models.TextField('Descripción')
    price = models.DecimalField('Precio', max_digits=10, decimal_places=2, null=True, blank=True,
                                help_text='Opcional. Si lo dejás vacío, no se muestra precio en la landing.')
    is_bookable = models.BooleanField('Reservable online', default=True,
                                      help_text='Si está activo, los pacientes pueden elegir este servicio al reservar. Desactivá para servicios solo informativos (charlas, workshops).')
    order = models.PositiveIntegerField('Orden', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Servicio'
        verbose_name_plural = 'Landing — Servicios'

    def __str__(self):
        return self.title

    @property
    def formatted_price(self):
        """Returns the price formatted for display, or '' if no price set.

        ARS uses dot for thousands and comma for decimals (Argentine convention):
        '$ 15.000' or '$ 1.500,50'. USD uses comma for thousands and dot for
        decimals: 'USD 1,200' or 'USD 25.50'.
        """
        if self.price is None:
            return ''
        currency = (self.professional.currency or 'ARS').upper()
        is_whole = self.price == self.price.to_integral_value()
        if currency == 'USD':
            return f'USD {int(self.price):,}' if is_whole else f'USD {self.price:,.2f}'
        # ARS: swap , and . (Python defaults to anglo format)
        if is_whole:
            return f'$ {int(self.price):,}'.replace(',', '.')
        anglo = f'{self.price:,.2f}'  # e.g. '1,500.50'
        return f'$ {anglo.replace(",", "X").replace(".", ",").replace("X", ".")}'


class LandingTestimonial(models.Model):
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='landing_testimonials')
    appointment = models.OneToOneField('Appointment', on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='testimonial',
                                       help_text='Si vino del flujo post-turno, queda atado al turno (1 reseña por turno).')
    quote = models.TextField('Texto del testimonio')
    author_name = models.CharField('Nombre del autor', max_length=100)
    author_meta = models.CharField('Detalle', max_length=100, blank=True, help_text='Ej: Paciente desde 2021')
    rating = models.PositiveSmallIntegerField('Estrellas (0-5)', default=5)
    is_approved = models.BooleanField('Aprobado', default=True,
                                      help_text='Las reseñas creadas vía link público arrancan en False hasta que el profesional las aprueba.')
    order = models.PositiveIntegerField('Orden', default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Testimonio'
        verbose_name_plural = 'Landing — Testimonios'

    def __str__(self):
        return f'{self.author_name} — {self.quote[:40]}'


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Agendado'),
        ('confirmed', 'Confirmado'),
        ('cancelled', 'Cancelado'),
        ('completed', 'Completado'),
    ]
    SOURCE_CHOICES = [
        ('online', 'Online'),
        ('manual', 'Manual'),
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
        ('phone', 'Teléfono'),
    ]
    MODE_CHOICES = [
        ('presencial', 'Presencial'),
        ('online',     'Online (videollamada)'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField('Fecha')
    appointment_time = models.TimeField('Hora')
    reason = models.TextField('Motivo', blank=True)
    status = models.CharField('Estado', max_length=50, choices=STATUS_CHOICES, default='scheduled')
    source = models.CharField('Origen', max_length=50, choices=SOURCE_CHOICES, default='online')
    mode = models.CharField('Modalidad', max_length=20, choices=MODE_CHOICES, default='presencial',
                            help_text='Presencial o videollamada. Si es online, se genera un link de Jitsi automáticamente.')
    meeting_url = models.URLField('Link de videollamada', blank=True, default='',
                                  help_text='Solo se completa cuando el turno es online.')
    notes = models.TextField('Notas del turno', blank=True, default='',
                             help_text='Notas privadas del profesional sobre este turno. Solo vos las ves.')
    service = models.ForeignKey('LandingService', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='appointments',
                                help_text='Servicio elegido. Si es null, se trata como consulta general.')
    price_at_booking = models.DecimalField('Precio al reservar', max_digits=10, decimal_places=2,
                                            null=True, blank=True,
                                            help_text='Precio congelado al momento de la reserva, independiente de cambios posteriores en el servicio.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Turno'
        verbose_name_plural = 'Turnos'
        unique_together = ['professional', 'appointment_date', 'appointment_time']
        ordering = ['appointment_date', 'appointment_time']

    def __str__(self):
        return f'{self.patient} - {self.appointment_date} {self.appointment_time}'

    def generate_meeting_url(self):
        """Returns a deterministic Jitsi room URL derived from this appointment's UUID.

        Same appointment always resolves to the same room, so the patient and the
        professional join the same call without coordinating room names.
        """
        room = f"consulte-{str(self.id).split('-')[0]}"
        return f"https://meet.jit.si/{room}"

    def save(self, *args, **kwargs):
        # uuid is assigned at __init__ (default=uuid.uuid4), so self.id is
        # always available here — no need for a two-step save.
        if self.mode == 'online' and not self.meeting_url:
            self.meeting_url = self.generate_meeting_url()
        super().save(*args, **kwargs)
