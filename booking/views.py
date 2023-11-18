from curses import start_color
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.views import View
from eruna import models
from booking.models import VacationBooking

class VacationBookingView(View):
    template = './booking/booking-travel.html'
    queryset = models.Destination

    def post(self, request, slug):
        if request.user.is_authenticated:
            destination = self.queryset.objects.filter(slug=slug).first()
        
            booking = VacationBooking(
                destination = destination,
                user_id = request.user.id,
                total_price = destination.price,
                start_date =  request.POST.get('start-date'),
                end_date = request.POST.get('end-date')
            )
            booking.save()
            return redirect(reverse('booking:bookings'))
        return redirect(reverse('auth_app:login'))


    def get(self, request):
        return redirect(reverse('eruna:destinations'))

class BookingListViews(View):
    template = './booking/bookings.html'

    def get(self, request):

        if request.user.is_authenticated:
            content_data = {
                'vacations' : VacationBooking.objects.filter(user_id=request.user.id)
            }

            return render(request, self.template, context=content_data)
        return redirect(reverse('auth_app:login'))