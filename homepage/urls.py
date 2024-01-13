from django.contrib import admin
from django.urls import path, include
from .views import *
urlpatterns = [
    path('', HomePageController.homepage),
    path('search', HomePageController.search),
    path('add_to_cart', CartController.add_to_cart),
    path('remove_from_cart', CartController.remove_from_cart),
    path('cart', CartController.get_cart_items)
]