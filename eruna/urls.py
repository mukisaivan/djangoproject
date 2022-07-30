from importlib.resources import path
from django.urls import path
from eruna import views

app_name = 'eruna'

urlpatterns = [
    path('', views.homePageView.as_view(), name='home'),
    path('destinations/', views.DestinationListView.as_view(), name='destinations'),
    path('destinations/<str:slug>', views.DestinationDetialView.as_view(), name='destination-detail'),
    path('cars/', views.CarListView.as_view(), name='cars'),
]