from django.db import migrations, models
from django.utils import timezone

class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0006_remove_reservation_reservation_datetime_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='created_at',
            field=models.DateTimeField(default=timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation',
            name='date',
            field=models.DateField(default=timezone.now().date()),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation',
            name='time',
            field=models.TimeField(default=timezone.now().time()),  # Provide a default value here
            preserve_default=False,
        ),
    ]
