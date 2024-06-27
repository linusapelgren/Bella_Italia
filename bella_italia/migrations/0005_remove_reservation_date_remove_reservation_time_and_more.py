from django.db import migrations, models
from django.utils import timezone

class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_remove_table_restaurant_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='date',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='time',
        ),
        migrations.AddField(
            model_name='reservation',
            name='reservation_datetime',
            field=models.DateTimeField(default=timezone.now),  # Corrected usage of timezone.now
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reservation',
            name='name',
            field=models.CharField(max_length=255),  # Updated max_length as per your model definition
        ),
    ]

