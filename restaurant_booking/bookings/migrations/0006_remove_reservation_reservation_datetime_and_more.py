from django.db import migrations, models
from django.utils import timezone

class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0005_remove_reservation_date_remove_reservation_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='reservation_datetime',
        ),
        migrations.AlterField(
            model_name='reservation',
            name='name',
            field=models.CharField(max_length=255),  # Ensure this matches your model definition
        ),
    ]
