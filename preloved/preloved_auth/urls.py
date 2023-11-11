from django.contrib import admin
from django.urls import path, include
from .views import new_shop_user

urlpatterns = [
    path('new_shop_user/', new_shop_user),

]
