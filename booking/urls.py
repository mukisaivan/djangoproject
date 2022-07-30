from django.urls import path
from booking import views

app_name = 'booking'

urlpatterns = [
    path('', views.BookingListViews.as_view(), name='bookings'),
    path('vacations/payment/', views.bookVacation, name='vacations-payment'),
    path('vacations/<str:slug>/', views.VacationBookingView.as_view(), name='vacations'),
    path('car/payment/', views.hireCar, name='car-payment'),
    path('cars/<str:slug>/', views.CarBookingView.as_view(), name='cars'),
]