from django.contrib import admin

from django.urls import path, include
from .views import new_shop_user, csrf_token, loginAPI, logout_attempt, is_logged_in

urlpatterns = [
    path('new_shop_user/', new_shop_user),
    path('csrf_token/', csrf_token),
    path('login/', loginAPI),
    path('logout/', logout_attempt),
    path('is_authenticated', is_logged_in)
]
