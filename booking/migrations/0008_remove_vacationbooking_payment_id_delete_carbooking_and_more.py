# Generated by Django 4.2.7 on 2023-11-18 13:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("booking", "0007_alter_vacationbooking_payment_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="vacationbooking",
            name="payment_id",
        ),
        migrations.DeleteModel(
            name="CarBooking",
        ),
        migrations.DeleteModel(
            name="Payment",
        ),
    ]
