from curses import start_color
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.views import View

from django.contrib import messages

import json
from eruna import models, views
from booking.models import VacationBooking, Payment, CarBooking

from paypalcheckoutsdk.orders import OrdersGetRequest
from .paypal import PayPalClient

from django.template import context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

def send_vacation_email(email, booking):
    context = {
        'email': email,
        'review': f"Hello, {email}",
        'booking': booking
    }
    email_subject = "Payment for {} with Eruna Safaris".format(booking.destination.name) 
    email_body = render_to_string('email/vacation_email_message.txt', context)

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, ['phillipmugisa9@gmail.com', ],
    )
    return email.send(fail_silently=False)

def send_car_email(email, booking):
    context = {
        'email': email,
        'review': f"Hello, {email}",
        'booking': booking
    }
    email_subject = "Car hire payment for {} with Eruna Safaris".format(booking.car.name) 
    email_body = render_to_string('email/car_email_message.txt', context)

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, ['phillipmugisa9@gmail.com', ],
    )
    return email.send(fail_silently=False)

class VacationBookingView(View):
    template = './booking/booking-travel.html'
    queryset = models.Destination

    def post(self, request, slug):
        if request.user.is_authenticated:
            destination = self.queryset.objects.filter(slug=slug).first()

            content_data = {
                'destination' : destination,
                'start_date' : request.POST.get('start-date'),
                'end_date' : request.POST.get('end-date'),
                'total_price' : destination.price
            }
            return render(request, self.template, context=content_data)
        return redirect(reverse('auth_app:login'))


    def get(self, request):
        return redirect(reverse('eruna:destinations'))


def bookVacation(request):
    if request.method == "POST":
        body = json.loads(request.body)

        order_id = body['orderID']
        destination_id = body['destinationID']
        start_date = body['startDate']
        end_date = body['endDate']
        mode_of_payment = body['mode_of_payment']

        destination = models.Destination.objects.filter(id=destination_id).first()

        user_id = request.user.id

        # get payment for paypal that matched the orderID
        PPClient = PayPalClient()
        requestorder = OrdersGetRequest(order_id)
        response = PPClient.client.execute(requestorder)

        receipt = Payment(
            user_id = user_id,
            mode_of_payment=mode_of_payment,
            total_amount_paid = response.result.purchase_units[0].amount.value,
            email = response.result.payer.email_address,
            address = response.result.purchase_units[0].shipping.address.address_line_1,
            country_code = response.result.purchase_units[0].shipping.address.country_code,
            order_key = response.result.id
        )
        receipt.save()

        booking = VacationBooking(
            destination = destination,
            user_id = user_id,
            total_price = receipt.total_amount_paid,
            start_date =  start_date,
            end_date = end_date,
            payment_id = receipt
        )
        booking.save()

        # send email
        send_vacation_email(email=response.result.payer.email_address, booking=booking)


        messages.add_message(request, messages.SUCCESS, 'Booking was successfull. A confirmation email was sent.')

        return HttpResponse(status=204)
    else:
        return redirect(reverse('eruna:destinations'))

class CarBookingView(View):
    template = './booking/booking-car.html'
    queryset = models.RentalCar

    def get(self, request, slug):
        if request.user.is_authenticated:
            car = self.queryset.objects.filter(slug=slug).first()
            images = models.CarImage.objects.filter(car=car)

            content_data = {
                'car' : car,
                'start_date' : request.POST.get('start-date'),
                'end_date' : request.POST.get('end-date'),
                'total_price' : car.price,
                'images': images
            }

            return render(request, self.template, context=content_data)
        return redirect(reverse('auth_app:login'))


class BookingListViews(View):
    template = './booking/bookings.html'

    def get(self, request):

        if request.user.is_authenticated:
            content_data = {
                'vacations' : VacationBooking.objects.filter(user_id=request.user.id),
                'cars' : CarBooking.objects.filter(user_id=request.user.id)
            }

            return render(request, self.template, context=content_data)
        return redirect(reverse('auth_app:login'))

def hireCar(request):
    if request.method == "POST":
        body = json.loads(request.body)

        order_id = body['orderID']
        car_id = body['carID']
        start_date = body['startDate']
        end_date = body['endDate']
        mode_of_payment = body['mode_of_payment']

        car = models.RentalCar.objects.filter(id=car_id).first()

        user_id = request.user.id

        # get payment for paypal that matched the orderID
        PPClient = PayPalClient()
        requestorder = OrdersGetRequest(order_id)
        response = PPClient.client.execute(requestorder)

        receipt = Payment(
            user_id = user_id,
            mode_of_payment=mode_of_payment,
            total_amount_paid = response.result.purchase_units[0].amount.value,
            email = response.result.payer.email_address,
            address = response.result.purchase_units[0].shipping.address.address_line_1,
            country_code = response.result.purchase_units[0].shipping.address.country_code,
            order_key = response.result.id
        )
        receipt.save()

        booking = CarBooking(
            car = car,
            user_id = user_id,
            total_price = receipt.total_amount_paid,
            start_date =  start_date,
            end_date = end_date,
            payment_id = receipt
        )
        booking.save()

        # send email
        send_car_email(email=response.result.payer.email_address, booking=booking)

        # make car unavailable
        car.is_available = False
        car.save()

        messages.add_message(request, messages.SUCCESS, 'Car Hired successfull. A confirmation email was sent.')

        return HttpResponse(status=204)
    else:
        return redirect(reverse('eruna:cars'))