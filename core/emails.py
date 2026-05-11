"""Transactional email via Resend.

Booking flow must never fail because of email — every send is wrapped in
try/except and logs the error. If RESEND_API_KEY is empty (dev, CI), the
function is a no-op.
"""
import logging

from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse

logger = logging.getLogger(__name__)


def _absolute_landing_url(professional, request=None):
    path = reverse('public_landing', kwargs={'slug': professional.slug})
    if request is not None:
        return request.build_absolute_uri(path)
    if settings.SITE_BASE_URL:
        return f'{settings.SITE_BASE_URL}{path}'
    return ''


def _absolute_profile_image_url(professional, request=None):
    if not professional.profile_image:
        return ''
    url = professional.profile_image.url
    if request is not None:
        return request.build_absolute_uri(url)
    if settings.SITE_BASE_URL:
        return f'{settings.SITE_BASE_URL}{url}'
    return ''


def send_appointment_confirmation(appointment, request=None):
    """Send the brand-book slide-20 confirmation email to the patient.

    Returns True if the API accepted the message, False otherwise (missing
    API key, missing patient email, or API error). Never raises.
    """
    api_key = settings.RESEND_API_KEY
    if not api_key:
        logger.info('Resend API key not set, skipping confirmation email.')
        return False

    patient = appointment.patient
    if not patient.email:
        return False

    professional = appointment.professional
    context = {
        'appointment': appointment,
        'patient': patient,
        'professional': professional,
        'landing_url': _absolute_landing_url(professional, request),
        'profile_image_url': _absolute_profile_image_url(professional, request),
    }

    subject = (
        f'Turno confirmado — {professional.professional_name} · '
        f'{appointment.appointment_date.strftime("%d/%m/%Y")} '
        f'{appointment.appointment_time.strftime("%H:%M")}'
    )
    html_body = render_to_string('core/emails/appointment_confirmation.html', context)
    text_body = render_to_string('core/emails/appointment_confirmation.txt', context)

    try:
        import resend
        resend.api_key = api_key
        resend.Emails.send({
            'from': settings.DEFAULT_FROM_EMAIL,
            'to': [patient.email],
            'subject': subject,
            'html': html_body,
            'text': text_body,
        })
        return True
    except Exception:
        logger.exception('Failed to send appointment confirmation email')
        return False
