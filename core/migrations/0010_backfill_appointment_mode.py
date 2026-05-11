"""Data migration: backfill Appointment.mode and meeting_url from Professional.attention_mode.

Rules:
- Professional.attention_mode contains "Online" (case-insensitive) and NOT "Presencial"
    → mode='online', meeting_url generated
- Anything else (including "Presencial y online" — too risky to retroactively
    generate URLs for past appointments without a per-appointment signal)
    → mode='presencial', no URL
"""
from django.db import migrations


def backfill_mode(apps, schema_editor):
    Appointment = apps.get_model('core', 'Appointment')

    for appointment in Appointment.objects.select_related('professional').all():
        attention = (appointment.professional.attention_mode or '').lower()
        if 'online' in attention and 'presencial' not in attention:
            appointment.mode = 'online'
            room = f"consulte-{str(appointment.id).split('-')[0]}"
            appointment.meeting_url = f"https://meet.jit.si/{room}"
        else:
            appointment.mode = 'presencial'
            appointment.meeting_url = ''
        appointment.save(update_fields=['mode', 'meeting_url'])


def reverse(apps, schema_editor):
    Appointment = apps.get_model('core', 'Appointment')
    Appointment.objects.update(mode='presencial', meeting_url='')


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_appointment_meeting_url_appointment_mode'),
    ]

    operations = [
        migrations.RunPython(backfill_mode, reverse),
    ]
