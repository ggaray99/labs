from django import forms
from .models import (
    Professional, Patient, Appointment,
    LandingStat, LandingCredential, LandingService, LandingTestimonial,
)


class ProfessionalSetupForm(forms.ModelForm):
    class Meta:
        model = Professional
        fields = ['professional_name', 'specialty', 'email', 'phone', 'address', 'bio',
                  'tagline', 'attention_mode', 'accepts_insurance', 'accepts_private',
                  'profile_image', 'common_reasons',
                  'working_days', 'start_time', 'end_time', 'appointment_duration_minutes']


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'phone', 'email', 'address',
                  'health_insurance', 'health_insurance_plan', 'health_insurance_number']


class BookingPatientForm(forms.Form):
    first_name = forms.CharField(max_length=255, label='Nombre')
    last_name = forms.CharField(max_length=255, label='Apellido')
    phone = forms.CharField(max_length=50, label='Teléfono')
    email = forms.EmailField(required=False, label='Email')
    health_insurance = forms.CharField(max_length=255, required=False, label='Obra social')
    health_insurance_plan = forms.CharField(max_length=255, required=False, label='Plan')
    health_insurance_number = forms.CharField(max_length=255, required=False, label='Nro. afiliado')
    reason = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label='Motivo de consulta')


class ManualAppointmentForm(forms.Form):
    patient_search = forms.CharField(max_length=255, required=False, label='Buscar paciente')
    first_name = forms.CharField(max_length=255, required=False, label='Nombre')
    last_name = forms.CharField(max_length=255, required=False, label='Apellido')
    phone = forms.CharField(max_length=50, required=False, label='Teléfono')
    email = forms.EmailField(required=False, label='Email')
    appointment_date = forms.DateField(label='Fecha')
    appointment_time = forms.TimeField(label='Hora')
    reason = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=False, label='Motivo')
    status = forms.ChoiceField(choices=Appointment.STATUS_CHOICES, initial='scheduled', label='Estado')


class ClinicalNotesForm(forms.Form):
    clinical_notes = forms.CharField(widget=forms.Textarea(attrs={'rows': 6}), required=False, label='Notas clínicas')


class MissionForm(forms.ModelForm):
    class Meta:
        model = Professional
        fields = ['mission']


class LandingSettingsForm(forms.ModelForm):
    class Meta:
        model = Professional
        fields = ['theme_primary', 'show_stats', 'show_credentials', 'show_mission',
                  'show_services', 'show_testimonials', 'show_contact']


class BasicsForm(forms.ModelForm):
    class Meta:
        model = Professional
        fields = ['professional_name', 'specialty', 'tagline', 'bio', 'profile_image']


class LandingStatForm(forms.ModelForm):
    class Meta:
        model = LandingStat
        fields = ['value', 'label', 'order']


class LandingCredentialForm(forms.ModelForm):
    class Meta:
        model = LandingCredential
        fields = ['icon', 'title', 'subtitle', 'order']


class LandingServiceForm(forms.ModelForm):
    class Meta:
        model = LandingService
        fields = ['icon', 'title', 'description', 'order']


class LandingTestimonialForm(forms.ModelForm):
    class Meta:
        model = LandingTestimonial
        fields = ['quote', 'author_name', 'author_meta', 'rating', 'order']
