import io
import base64
from datetime import datetime, timedelta, date

import qrcode
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import signing
from django.db.models import Q
from django.urls import reverse

from .models import (
    Professional, Patient, Appointment,
    LandingStat, LandingCredential, LandingService, LandingTestimonial,
)
from .forms import (
    ProfessionalSetupForm, BookingPatientForm, PatientForm,
    MissionForm, LandingSettingsForm, BasicsForm, LandingStatForm, LandingCredentialForm,
    LandingServiceForm, LandingTestimonialForm, PublicReviewForm,
)


REVIEW_TOKEN_SALT = 'clyra.appointment.review'
REVIEW_TOKEN_MAX_AGE = 60 * 24 * 60 * 60  # 60 days


def make_review_token(appointment):
    return signing.TimestampSigner(salt=REVIEW_TOKEN_SALT).sign(str(appointment.id))


def parse_review_token(token):
    try:
        appointment_id = signing.TimestampSigner(salt=REVIEW_TOKEN_SALT).unsign(
            token, max_age=REVIEW_TOKEN_MAX_AGE
        )
    except signing.BadSignature:
        return None
    return Appointment.objects.filter(id=appointment_id).first()


# --- Helpers ---

def get_professional(request):
    """Get the professional linked to the logged-in user."""
    try:
        return request.user.professional
    except Professional.DoesNotExist:
        return None


def generate_qr_base64(url):
    qr = qrcode.make(url, box_size=6, border=2)
    buffer = io.BytesIO()
    qr.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode()


def get_available_slots(professional, target_date):
    start = datetime.combine(target_date, professional.start_time)
    end = datetime.combine(target_date, professional.end_time)
    duration = timedelta(minutes=professional.appointment_duration_minutes)

    existing = set(
        Appointment.objects.filter(
            professional=professional,
            appointment_date=target_date,
            status__in=['scheduled', 'confirmed']
        ).values_list('appointment_time', flat=True)
    )

    slots = []
    current = start
    while current + duration <= end:
        t = current.time()
        if t not in existing:
            slots.append(t)
        current += duration
    return slots


DAYS_MAP = {
    'lunes': 0, 'martes': 1, 'miercoles': 2, 'miércoles': 2,
    'jueves': 3, 'viernes': 4, 'sabado': 5, 'sábado': 5, 'domingo': 6,
}

DAYS_LIST = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']


# --- Public Views ---

def home(request):
    if request.user.is_authenticated and hasattr(request.user, 'professional'):
        return redirect('dashboard')
    return render(request, 'core/home.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        # Django auth uses username, we find user by email
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            return render(request, 'core/login.html', {'error': 'Email o contraseña incorrectos.'})

    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def setup(request):
    if request.user.is_authenticated and hasattr(request.user, 'professional'):
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')

        errors = []

        if not password or len(password) < 6:
            errors.append('La contraseña debe tener al menos 6 caracteres.')
        if password != password_confirm:
            errors.append('Las contraseñas no coinciden.')
        if User.objects.filter(email=email).exists():
            errors.append('Ya existe una cuenta con ese email.')

        working_days = ','.join(request.POST.getlist('working_days'))
        post_data = request.POST.copy()
        post_data['accepts_insurance'] = 'accepts_insurance' in request.POST
        post_data['accepts_private'] = 'accepts_private' in request.POST
        form = ProfessionalSetupForm(post_data, request.FILES)

        if form.is_valid() and not errors:
            # Create User
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
            )
            # Create Professional linked to User
            professional = form.save(commit=False)
            professional.user = user
            professional.working_days = working_days
            professional.save()

            login(request, user)
            messages.success(request, 'Tu consultorio ya está online.')
            return redirect('dashboard')

        form_errors = [e for field_errors in form.errors.values() for e in field_errors]
        errors.extend(form_errors)
        return render(request, 'core/setup.html', {'form': form, 'days': DAYS_LIST, 'errors': errors})

    form = ProfessionalSetupForm()
    return render(request, 'core/setup.html', {'form': form, 'days': DAYS_LIST})


# --- Dashboard Views (all require login) ---

@login_required
def dashboard(request):
    professional = get_professional(request)
    if not professional:
        return redirect('setup')

    today = date.today()
    appointments_today = list(Appointment.objects.filter(
        professional=professional,
        appointment_date=today
    ).select_related('patient'))

    upcoming = Appointment.objects.filter(
        professional=professional,
        appointment_date__gte=today,
        status__in=['scheduled', 'confirmed']
    ).select_related('patient').order_by('appointment_date', 'appointment_time')[:10]

    recent_patients = Patient.objects.filter(professional=professional).order_by('-created_at')[:5]

    public_url = request.build_absolute_uri(f'/p/{professional.slug}/')
    qr_data = generate_qr_base64(public_url)

    # Attach review_link to completed appointments missing a testimonial.
    for apt in appointments_today:
        apt.review_link = ''
        if apt.status == 'completed' and not hasattr(apt, 'testimonial'):
            apt.review_link = request.build_absolute_uri(
                reverse('public_review', kwargs={'slug': professional.slug, 'token': make_review_token(apt)})
            )

    return render(request, 'core/dashboard.html', {
        'professional': professional,
        'appointments_today': appointments_today,
        'upcoming': upcoming,
        'recent_patients': recent_patients,
        'public_url': public_url,
        'qr_data': qr_data,
        'today': today,
        'status_choices': Appointment.STATUS_CHOICES,
    })


@login_required
def appointment_new(request):
    professional = get_professional(request)
    if not professional:
        return redirect('setup')

    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        patient = None

        if patient_id:
            patient = Patient.objects.filter(id=patient_id, professional=professional).first()

        if not patient:
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            phone = request.POST.get('phone', '').strip()
            if first_name and last_name and phone:
                patient, _ = Patient.objects.update_or_create(
                    professional=professional,
                    phone=phone,
                    defaults={'first_name': first_name, 'last_name': last_name, 'email': request.POST.get('email', '')}
                )

        if patient:
            apt_date = request.POST.get('appointment_date')
            apt_time = request.POST.get('appointment_time')
            try:
                d = datetime.strptime(apt_date, '%Y-%m-%d').date()
                t = datetime.strptime(apt_time, '%H:%M').time()
                if Appointment.objects.filter(
                    professional=professional, appointment_date=d, appointment_time=t,
                    status__in=['scheduled', 'confirmed']
                ).exists():
                    messages.error(request, 'Ya existe un turno en ese horario.')
                else:
                    Appointment.objects.create(
                        professional=professional, patient=patient,
                        appointment_date=d, appointment_time=t,
                        reason=request.POST.get('reason', ''),
                        status=request.POST.get('status', 'scheduled'),
                        source='manual',
                    )
                    messages.success(request, 'Turno creado correctamente.')
                    return redirect('dashboard')
            except (ValueError, TypeError):
                messages.error(request, 'Fecha u hora inválida.')

    patients = Patient.objects.filter(professional=professional).order_by('last_name', 'first_name')
    return render(request, 'core/appointment_new.html', {
        'professional': professional,
        'patients': patients,
        'status_choices': Appointment.STATUS_CHOICES,
    })


@login_required
def appointment_status(request, appointment_id):
    professional = get_professional(request)
    if not professional:
        return redirect('setup')

    appointment = get_object_or_404(Appointment, id=appointment_id, professional=professional)
    new_status = request.POST.get('status')
    if new_status in dict(Appointment.STATUS_CHOICES):
        appointment.status = new_status
        appointment.save()
    return redirect('dashboard')


@login_required
def patient_list(request):
    professional = get_professional(request)
    if not professional:
        return redirect('setup')

    q = request.GET.get('q', '')
    patients = Patient.objects.filter(professional=professional)
    if q:
        patients = patients.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q) |
            Q(phone__icontains=q) | Q(email__icontains=q)
        )
    patients = patients.order_by('last_name', 'first_name')

    return render(request, 'core/patient_list.html', {
        'professional': professional,
        'patients': patients,
        'q': q,
    })


@login_required
def patient_detail(request, patient_id):
    professional = get_professional(request)
    if not professional:
        return redirect('setup')

    patient = get_object_or_404(Patient, id=patient_id, professional=professional)
    appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date', '-appointment_time')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_info':
            form = PatientForm(request.POST, instance=patient)
            if form.is_valid():
                form.save()
                messages.success(request, 'Datos actualizados.')
                return redirect('patient_detail', patient_id=patient.id)

        elif action == 'update_notes':
            patient.clinical_notes = request.POST.get('clinical_notes', '')
            patient.save()
            messages.success(request, 'Notas clínicas actualizadas.')
            return redirect('patient_detail', patient_id=patient.id)

    return render(request, 'core/patient_detail.html', {
        'professional': professional,
        'patient': patient,
        'appointments': appointments,
    })


@login_required
def patient_new(request):
    professional = get_professional(request)
    if not professional:
        return redirect('setup')

    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.professional = professional
            patient.save()
            messages.success(request, 'Paciente creado.')
            return redirect('patient_detail', patient_id=patient.id)
    else:
        form = PatientForm()

    return render(request, 'core/patient_new.html', {
        'professional': professional,
        'form': form,
    })


@login_required
def patient_search_api(request):
    professional = get_professional(request)
    if not professional:
        return JsonResponse([], safe=False)

    q = request.GET.get('q', '')
    if len(q) < 2:
        return JsonResponse([], safe=False)

    patients = Patient.objects.filter(
        professional=professional
    ).filter(
        Q(first_name__icontains=q) | Q(last_name__icontains=q) |
        Q(phone__icontains=q) | Q(email__icontains=q)
    )[:10]

    results = [{'id': str(p.id), 'name': f'{p.first_name} {p.last_name}', 'phone': p.phone} for p in patients]
    return JsonResponse(results, safe=False)


# --- Landing Admin (per-professional editor) ---

LANDING_SECTIONS = {
    'stat':        (LandingStat,         LandingStatForm,         'landing_stats'),
    'credential':  (LandingCredential,   LandingCredentialForm,   'landing_credentials'),
    'service':     (LandingService,      LandingServiceForm,      'landing_services'),
    'testimonial': (LandingTestimonial,  LandingTestimonialForm,  'landing_testimonials'),
}


@login_required
def landing_admin(request):
    professional = get_professional(request)
    if not professional:
        return redirect('setup')

    if request.method == 'POST':
        action = request.POST.get('action', '')

        if action == 'mission_save':
            form = MissionForm(request.POST, instance=professional)
            if form.is_valid():
                form.save()
                messages.success(request, 'Misión actualizada.')
            return redirect('/dashboard/landing/#mission')

        if action == 'settings_save':
            form = LandingSettingsForm(request.POST, instance=professional)
            if form.is_valid():
                form.save()
                messages.success(request, 'Ajustes de landing guardados.')
            else:
                messages.error(request, 'Color inválido.')
            return redirect('/dashboard/landing/#settings')

        if action == 'basics_save':
            form = BasicsForm(request.POST, request.FILES, instance=professional)
            if form.is_valid():
                form.save()
                messages.success(request, 'Datos básicos actualizados.')
            else:
                messages.error(request, 'Revisá los campos.')
            return redirect('/dashboard/landing/#basics')

        if action == 'testimonial_approve':
            obj = get_object_or_404(LandingTestimonial, id=request.POST.get('id'), professional=professional)
            obj.is_approved = True
            obj.save()
            messages.success(request, 'Reseña aprobada y publicada.')
            return redirect('/dashboard/landing/#testimonials')

        # Format: <section>_<verb> with verb in {add, save, delete}
        for section, (Model, FormCls, _) in LANDING_SECTIONS.items():
            anchor = f'/dashboard/landing/#{section}s'
            if action == f'{section}_add':
                instance = Model(professional=professional)
                form = FormCls(request.POST, instance=instance)
                if form.is_valid():
                    form.save()
                    messages.success(request, f'Item agregado.')
                else:
                    messages.error(request, 'No se pudo guardar. Revisá los campos.')
                return redirect(anchor)

            if action == f'{section}_save':
                obj = get_object_or_404(Model, id=request.POST.get('id'), professional=professional)
                form = FormCls(request.POST, instance=obj)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Cambios guardados.')
                return redirect(anchor)

            if action == f'{section}_delete':
                obj = get_object_or_404(Model, id=request.POST.get('id'), professional=professional)
                obj.delete()
                messages.success(request, 'Item eliminado.')
                return redirect(anchor)

    testimonials_qs = professional.landing_testimonials.all()
    return render(request, 'core/landing_admin.html', {
        'professional': professional,
        'stats': professional.landing_stats.all(),
        'credentials': professional.landing_credentials.all(),
        'services': professional.landing_services.all(),
        'testimonials': testimonials_qs.filter(is_approved=True),
        'pending_testimonials': testimonials_qs.filter(is_approved=False),
        'public_url': request.build_absolute_uri(f'/p/{professional.slug}/'),
    })


# --- Public Landing & Booking ---

def public_landing(request, slug):
    professional = get_object_or_404(Professional, slug=slug)

    # Booking data for inline section
    selected_date_str = request.GET.get('date') or request.POST.get('date')
    working_day_nums = {DAYS_MAP[d] for d in professional.get_working_days_list() if d in DAYS_MAP}
    available_dates = []
    for i in range(1, 30):
        d = date.today() + timedelta(days=i)
        if d.weekday() in working_day_nums:
            available_dates.append(d)
        if len(available_dates) >= 14:
            break

    selected_date = None
    slots = []
    if selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
            slots = get_available_slots(professional, selected_date)
        except ValueError:
            pass

    # Handle booking POST
    if request.method == 'POST' and 'first_name' in request.POST:
        form = BookingPatientForm(request.POST)
        selected_time_str = request.POST.get('time')
        if form.is_valid() and selected_date and selected_time_str:
            selected_time = datetime.strptime(selected_time_str, '%H:%M').time()
            if Appointment.objects.filter(
                professional=professional, appointment_date=selected_date,
                appointment_time=selected_time, status__in=['scheduled', 'confirmed']
            ).exists():
                messages.error(request, 'Este horario ya no está disponible.')
                return redirect('public_landing', slug=slug)

            data = form.cleaned_data
            patient, _ = Patient.objects.update_or_create(
                professional=professional, phone=data['phone'],
                defaults={
                    'first_name': data['first_name'], 'last_name': data['last_name'],
                    'email': data.get('email', ''),
                    'health_insurance': data.get('health_insurance', ''),
                    'health_insurance_plan': data.get('health_insurance_plan', ''),
                    'health_insurance_number': data.get('health_insurance_number', ''),
                }
            )
            Appointment.objects.create(
                professional=professional, patient=patient,
                appointment_date=selected_date, appointment_time=selected_time,
                reason=data.get('reason', ''), source='online',
            )
            return render(request, 'core/booking_confirmation.html', {
                'professional': professional, 'date': selected_date, 'time': selected_time,
            })

    form = BookingPatientForm()
    return render(request, 'core/public_landing.html', {
        'professional': professional,
        'available_dates': available_dates,
        'selected_date': selected_date,
        'slots': slots,
        'form': form,
        'landing_stats': professional.landing_stats.all(),
        'landing_credentials': professional.landing_credentials.all(),
        'landing_services': professional.landing_services.all(),
        'landing_testimonials': professional.landing_testimonials.filter(is_approved=True),
    })


def booking(request, slug):
    """Legacy redirect — booking is now inline in public_landing."""
    return redirect('public_landing', slug=slug)


def public_review(request, slug, token):
    professional = get_object_or_404(Professional, slug=slug)
    appointment = parse_review_token(token)

    if not appointment or appointment.professional_id != professional.id:
        return render(request, 'core/review.html', {
            'professional': professional, 'invalid': True,
        })

    if hasattr(appointment, 'testimonial'):
        return render(request, 'core/review.html', {
            'professional': professional, 'already_submitted': True,
        })

    if request.method == 'POST':
        form = PublicReviewForm(request.POST)
        if form.is_valid():
            patient = appointment.patient
            author_name = f'{patient.first_name} {patient.last_name[:1].upper()}.'
            LandingTestimonial.objects.create(
                professional=professional,
                appointment=appointment,
                quote=form.cleaned_data['quote'],
                rating=form.cleaned_data['rating'],
                author_name=author_name,
                author_meta=f'Paciente — {appointment.appointment_date.strftime("%m/%Y")}',
                is_approved=False,
            )
            return render(request, 'core/review.html', {
                'professional': professional, 'success': True,
            })
    else:
        form = PublicReviewForm()

    return render(request, 'core/review.html', {
        'professional': professional,
        'appointment': appointment,
        'form': form,
    })
