from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('restaurant/', views.restaurant_detail, name='restaurant_detail'),
    path('reserve/', views.make_reservation, name='make_reservation'),
    path('reservation/confirmation/', views.reservation_confirmation, name='reservation_confirmation'),
    path('restaurant/menu/', views.menu, name='menu'),
]
