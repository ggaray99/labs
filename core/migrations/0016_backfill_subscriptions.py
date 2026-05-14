from django.db import migrations


def create_subscriptions_for_existing_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Subscription = apps.get_model('core', 'Subscription')
    for user in User.objects.all():
        Subscription.objects.get_or_create(user=user, defaults={'plan': 'free', 'status': 'active'})


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0015_subscription'),
    ]

    operations = [
        migrations.RunPython(create_subscriptions_for_existing_users, noop),
    ]
