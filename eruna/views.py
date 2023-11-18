from django.shortcuts import render
from django.views import View
from django.db.models import Q
from django.core.paginator import Paginator

from booking.models import VacationBooking

from eruna import models

# Create your views here.
class DestinationListView(View):
    template = './eruna/destinations.html'
    queryset = models.Destination

    def get(self, request, *args, **kwargs):

        PER_PAGE_COUNT = 6

        paginator = Paginator(self.queryset.objects.all().order_by('-id'), PER_PAGE_COUNT)

        # get current page number
        page_num = request.GET.get('page', 1)
        destinations = paginator.page(page_num).object_list
        if self.queryset.objects.all().count() > 0:


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
        # if VacationBooking.objects.filter(Q(user_id = request.user.id), Q(destination = destination) | Q(is_complete = False)):
        #     booking_exists = True

        content_data = {
            'destination' : destination,
            'images' : images,
            'booking_exists' : booking_exists
        }

        return render(request, self.template, context=content_data)
