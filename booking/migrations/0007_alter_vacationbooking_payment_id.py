# Generated by Django 4.2.7 on 2023-11-18 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("booking", "0006_alter_carbooking_payment_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vacationbooking",
            name="payment_id",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="booking.payment",
            ),
        ),
    ]