from pyexpat import model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
import os
import uuid

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(f'images/{instance.__class__.__name__}', filename)

class Destination(models.Model):
    name = models.CharField(
        _('Destination Name'),
        max_length=256
    )
    description = models.TextField(
        _('Destination Description')
    )
    location = models.CharField(
        _('Destination Location'),
        max_length=256
    )
    price = models.IntegerField(
        _('Cost of Vacation')
    )
    distance = models.IntegerField(
        _('Distance From Kampala'),
        blank=True,
        null=True
    )
    slug = models.SlugField(
        _("Safe Url"),
        unique=True,
        blank = True,
        null = True,
    )
    related_url = models.URLField(
        _('Url To Related Article'),
        blank=True,
        null=True,
    )
    added_on = models.DateTimeField(
        _("Upload On"),
        default=timezone.now,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        self.name = self.name.title()

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.name}'


class DestinationImage(models.Model):
    destination = models.ForeignKey(
        to=Destination,
        on_delete=models.CASCADE
    )
    img_url = models.ImageField(
        _('Image Url'),
        blank=True,
        null=True,
        upload_to=get_file_path
    )
    online_url = models.URLField(
        _('Online Image Url'),
        blank=True,
        null=True,
    )
    added_on = models.DateTimeField(
        _("Upload On"),
        default=timezone.now,
    )

    def __str__(self) -> str:
        return f'{self.destination.name}'


class RentalCar(models.Model):
    name = models.CharField(
        _('Car Name'),
        max_length=256
    )
    reg_no = models.CharField(
        _('Car Registration Number'),
        max_length=256
    )
    owner = models.CharField(
        _('Car Owner'),
        max_length=256,
        default='Admin'
    )
    seats = models.IntegerField(
        _('Number of Seats')
    )
    price = models.DecimalField(
        _('Cost of hire'),
        decimal_places=2,
        max_digits=6
    )
    is_available = models.BooleanField(
        _('Is Available'),
        default=True
    )
    slug = models.SlugField(
        _("Safe Url"),
        unique=True,
        blank = True,
        null = True,
    )
    added_on = models.DateTimeField(
        _("Upload On"),
        default=timezone.now,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        self.name = self.name.title()

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.name}'

class CarImage(models.Model):
    car = models.ForeignKey(
        to=RentalCar,
        on_delete=models.CASCADE
    )
    img_url = models.ImageField(
        _('Image Url'),
        upload_to=get_file_path
    )
    added_on = models.DateTimeField(
        _("Upload On"),
        default=timezone.now,
    )

    def __str__(self) -> str:
        return f'{self.car.name}'


class Lounge(models.Model):
    name = models.CharField(
        _('Destination Name'),
        max_length=256
    )
    description = models.TextField(
        _('Destination Description')
    )
    location = models.CharField(
        _('Destination Location'),
        max_length=256
    )
    price = models.DecimalField(
        _('Cost of Vacation'),
        decimal_places=2,
        max_digits=6
    )
    distance = models.IntegerField(
        _('Distance From Kampala'),
        blank=True,
        null=True
    )
    room_count = models.IntegerField(
        _('Number of Rooms')
    )
    slug = models.SlugField(
        _("Safe Url"),
        unique=True,
        blank = True,
        null = True,
    )
    related_url = models.URLField(
        _('Url To Related Article'),
        blank=True,
        null=True,
    )

    added_on = models.DateTimeField(
        _("Upload On"),
        default=timezone.now,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        self.name = self.name.title()

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.name}'

class LoungeImage(models.Model):
    lounge = models.ForeignKey(
        to=Lounge,
        on_delete=models.CASCADE
    )
    img_url = models.ImageField(
        _('Image Url'),
        upload_to=get_file_path
    )
    added_on = models.DateTimeField(
        _("Upload On"),
        default=timezone.now,
    )

    def __str__(self) -> str:
        return f'{self.lounge.name}'

class TravelMoment(models.Model):
    destination = models.CharField(
        _('Destination Name'),
        max_length=256
    )
    slug = models.SlugField(
        _("Safe Url"),
        unique=True,
        blank = True,
        null = True,
    )
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        self.name = self.name.title()

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.destination}'

class TravelMomentImage(models.Model):
    travel_moment = models.ForeignKey(
        to=TravelMoment,
        on_delete=models.CASCADE
    )
    img_url = models.ImageField(
        _('Image Url'),
        upload_to=get_file_path
    )
    added_on = models.DateTimeField(
        _("Upload On"),
        default=timezone.now,
    )

    def __str__(self) -> str:
        return f'{self.travel_moment.name}'