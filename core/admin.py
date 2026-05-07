from django.contrib import admin
from .models import (
    Professional, Patient, Appointment,
    LandingStat, LandingCredential, LandingService, LandingTestimonial,
)


class LandingStatInline(admin.TabularInline):
    model = LandingStat
    extra = 1
    fields = ['order', 'value', 'label']
    ordering = ['order']


class LandingCredentialInline(admin.TabularInline):
    model = LandingCredential
    extra = 1
    fields = ['order', 'icon', 'title', 'subtitle']
    ordering = ['order']


class LandingServiceInline(admin.TabularInline):
    model = LandingService
    extra = 1
    fields = ['order', 'icon', 'title', 'description']
    ordering = ['order']


class LandingTestimonialInline(admin.TabularInline):
    model = LandingTestimonial
    extra = 1
    fields = ['order', 'rating', 'quote', 'author_name', 'author_meta']
    ordering = ['order']


@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ['professional_name', 'specialty', 'email', 'slug', 'attention_mode']
    search_fields = ['professional_name', 'email']
    fieldsets = [
        ('Datos básicos', {'fields': ['professional_name', 'specialty', 'email', 'phone', 'address', 'slug']}),
        ('Perfil público', {'fields': ['tagline', 'bio', 'profile_image', 'attention_mode', 'accepts_insurance', 'accepts_private', 'common_reasons']}),
        ('Landing — Misión', {'fields': ['mission'], 'description': 'Frase destacada que se muestra en la tarjeta azul de la landing.'}),
        ('Agenda', {'fields': ['working_days', 'start_time', 'end_time', 'appointment_duration_minutes']}),
    ]
    inlines = [LandingStatInline, LandingCredentialInline, LandingServiceInline, LandingTestimonialInline]


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'health_insurance', 'professional']
    search_fields = ['first_name', 'last_name', 'phone']
    list_filter = ['professional']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'appointment_date', 'appointment_time', 'status', 'source']
    list_filter = ['status', 'source', 'appointment_date']
