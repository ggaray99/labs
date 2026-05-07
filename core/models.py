import uuid
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils.text import slugify

HEX_COLOR_VALIDATOR = RegexValidator(r'^#(?:[0-9a-fA-F]{3}){1,2}$', 'Color en formato hex. Ej: #3B82F6')


class Professional(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='professional', null=True)
    professional_name = models.CharField('Nombre completo', max_length=255)
    specialty = models.CharField('Especialidad', max_length=255)
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
    theme_primary = models.CharField('Color principal', max_length=7, default='#004ac6', validators=[HEX_COLOR_VALIDATOR],
                                     help_text='Color de CTAs, links y tarjeta de misión.')
    show_stats = models.BooleanField('Mostrar estadísticas', default=True)
    show_credentials = models.BooleanField('Mostrar credenciales', default=True)
    show_mission = models.BooleanField('Mostrar misión', default=True)
    show_services = models.BooleanField('Mostrar servicios', default=True)
    show_testimonials = models.BooleanField('Mostrar testimonios', default=True)
    show_contact = models.BooleanField('Mostrar sección de contacto', default=True)
    show_map = models.BooleanField('Mostrar mapa de ubicación', default=True,
                                   help_text='Solo se renderiza si además hay una dirección cargada.')
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
    order = models.PositiveIntegerField('Orden', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Servicio'
        verbose_name_plural = 'Landing — Servicios'

    def __str__(self):
        return self.title


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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField('Fecha')
    appointment_time = models.TimeField('Hora')
    reason = models.TextField('Motivo', blank=True)
    status = models.CharField('Estado', max_length=50, choices=STATUS_CHOICES, default='scheduled')
    source = models.CharField('Origen', max_length=50, choices=SOURCE_CHOICES, default='online')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Turno'
        verbose_name_plural = 'Turnos'
        unique_together = ['professional', 'appointment_date', 'appointment_time']
        ordering = ['appointment_date', 'appointment_time']

    def __str__(self):
        return f'{self.patient} - {self.appointment_date} {self.appointment_time}'
