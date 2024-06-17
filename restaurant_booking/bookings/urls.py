from django.urls import path
from . import views

urlpatterns = [
    path('', views.restaurant_list, name='restaurant_list'),
    path('restaurant/<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('reserve/', views.make_reservation, name='make_reservation'),
    path('reservation/<int:pk>/confirmation/', views.reservation_confirmation, name='reservation_confirmation'),
    path('restaurant/<int:pk>/menu/', views.menu, name='menu'),
]
