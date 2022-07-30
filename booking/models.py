from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
import os
import uuid

from eruna.models import Destination, RentalCar

class VacationBooking(models.Model):
    destination = models.ForeignKey(
        to=Destination,
        on_delete=models.CASCADE
    )
    user_id = models.IntegerField(
        _('User Id'),
        default='1'
    )
    total_price = models.DecimalField(
        _('Total Price'),
        decimal_places=2,
        max_digits=8
    )
    start_date = models.DateField(
        _('Start Date')
    )
    end_date = models.DateField(
        _('End Date')
    )
    is_complete = models.BooleanField(
        _("Vacation is complete"),
        default=False
    )
    payment_id = models.OneToOneField(
        to='Payment',
        on_delete=models.CASCADE
    )
    added_on = models.DateTimeField(
        _("Upload On"),
        default=timezone.now,
        editable=False
    )
    def __str__(self) -> str:
        return f'{self.destination.name}'

class CarBooking(models.Model):
    car = models.ForeignKey(
        to=RentalCar,
        on_delete=models.CASCADE
    )
    user_id = models.IntegerField(
        _('User Id'),
        default='1'
    )
    total_price = models.DecimalField(
        _('Total Price'),
        decimal_places=2,
        max_digits=8
    )
    start_date = models.DateField(
        _('Start Date')
    )
    end_date = models.DateField(
        _('End Date')
    )
    is_returned = models.BooleanField(
        _("Car is returned"),
        default=False
    )
    payment_id = models.OneToOneField(
        to='Payment',
        on_delete=models.CASCADE
    )
    added_on = models.DateTimeField(
        _("Upload On"),
        default=timezone.now,
        editable=False
    )
    def __str__(self) -> str:
        return f'{self.car.name}'

class Payment(models.Model):
    user_id = models.IntegerField(
        _('User Id')
    )
    mode_of_payment = models.CharField(
        _('Mode of Payment'),
        max_length=256
    )
    total_amount_paid =  models.DecimalField(
        _("Total Amount Paid"),
        decimal_places=2,
        max_digits=8
    )
    email = models.CharField(
        _("Client's Email"),
        max_length=256
    )
    country_code = models.CharField(
        _("Client's Country"),
        max_length=9
    )
    address = models.CharField(
        _("Client's Address"),
        max_length=256
    )
    order_key = models.CharField(
        _("Order key"),
        max_length=256
    )
    paid_on = models.DateTimeField(
        _("Paid On"),
        default=timezone.now,
        editable=False
    )