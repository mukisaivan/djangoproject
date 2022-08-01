from django.shortcuts import render
from django.views import View
from django.db.models import Q
from django.core.paginator import Paginator

from eruna import models

from booking.models import VacationBooking, CarBooking

# Create your views here.
class homePageView(View):
    template = 'eruna/index.html'

    def get(self, request, *args, **kwargs):

        SLICE_UPPER = 6
        SLICE_LOWER = 0

        destinations = models.Destination.objects.all().order_by('-id')[:SLICE_UPPER]
        cars = models.RentalCar.objects.all().order_by('-id')[:SLICE_UPPER]


        destination_cover_imgs = []
        if models.Destination.objects.all().count() > 0:
            # get first image for each of the first 6 destinations
            destination_cover_imgs = models.DestinationImage.objects.filter(
                Q(destination__id__gte = destinations[len(destinations) - 1].id),
                Q(destination__id__lte = destinations[SLICE_LOWER].id)
            )
            
        car_cover_imgs = []
        if models.RentalCar.objects.all().count() > 0:
            car_cover_imgs = models.CarImage.objects.filter(
                Q(car__id__gte = cars[len(cars) - 1].id),
                Q(car__id__lte = cars[SLICE_LOWER].id)
            )

        content_data = {
            'page' : 'home',
            'destinations' : destinations,
            'destination_cover_imgs': destination_cover_imgs,
            'cars' : cars,
            'car_cover_imgs': car_cover_imgs,
            'travel_moments' : models.TravelMoment.objects.all().order_by('-id')[:6],
        }

        return render(request, self.template, context=content_data)

class DestinationListView(View):
    template = './eruna/destinations.html'
    queryset = models.Destination

    def get(self, request, *args, **kwargs):

        PER_PAGE_COUNT = 6

        paginator = Paginator(self.queryset.objects.all().order_by('-id'), PER_PAGE_COUNT)

        if self.queryset.objects.all().count() > 0:

            # get current page number
            page_num = request.GET.get('page', 1)
            destinations = paginator.page(page_num).object_list

            destination_cover_imgs = models.DestinationImage.objects.filter(
                Q(destination__id__gte = destinations[len(destinations) - 1].id),
                Q(destination__id__lte = destinations[0].id)
            )

        else:
            destination_cover_imgs = []

        content_data = {
            'page_obj': paginator.page(page_num),
            'destinations' : destinations,
            'destination_cover_imgs': destination_cover_imgs,
        }

        return render(request, self.template, context=content_data)

class DestinationDetialView(View):
    template = './eruna/destination.html'
    queryset = models.Destination

    def get(self, request, slug):
        destination = self.queryset.objects.filter(slug=slug).first()
        images = models.DestinationImage.objects.filter(destination=destination)

        booking_exists = False
        if VacationBooking.objects.filter(Q(user_id = request.user.id), Q(destination = destination) | Q(is_complete = False)):
            booking_exists = True


        content_data = {
            'destination' : destination,
            'images' : images,
            'booking_exists' : booking_exists
        }

        return render(request, self.template, context=content_data)

class CarListView(View):
    template = './eruna/cars.html'
    queryset = models.RentalCar

    def get(self, request, *args, **kwargs):

        PER_PAGE_COUNT = 6

        paginator = Paginator(self.queryset.objects.filter(is_available=True).order_by('-id'), PER_PAGE_COUNT)

        # get current page number
        page_num = request.GET.get('page', 1)
        cars = paginator.page(page_num).object_list

        car_cover_imgs = models.CarImage.objects.filter(
            Q(car__id__gte = cars[len(cars) - 1].id),
            Q(car__id__lte = cars[0].id)
        )

        content_data = {
            'page_obj': paginator.page(page_num),
            'cars' : cars,
            'car_cover_imgs': car_cover_imgs,
        }

        return render(request, self.template, context=content_data)