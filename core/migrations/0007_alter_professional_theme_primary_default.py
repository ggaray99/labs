from django.db import migrations, models
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_landingtestimonial_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professional',
            name='theme_primary',
            field=models.CharField(
                default='#0047ab',
                help_text='Color de CTAs, links y tarjeta de misión.',
                max_length=7,
                validators=[core.models.HEX_COLOR_VALIDATOR],
                verbose_name='Color principal',
            ),
        ),
    ]
