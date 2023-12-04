from django.contrib import admin

from django.urls import path, include
from .views import new_shop_user, csrf_token, loginAPI, logout_attempt, is_logged_in, shop_id_selfie, shop_id_two, shop_id_one, new_shop_owner, get_image, document_status, get_shop_owner_details, get_list_pending
from .views import approve_or_reject, get_current_user
urlpatterns = [
    path('new_shop_user', new_shop_user),
    path('csrf_token', csrf_token),
    path('login', loginAPI),
    path('logout', logout_attempt),
    path('is_authenticated', is_logged_in),
    path('shop_id_one', shop_id_one),
    path('shop_id_two', shop_id_two),
    path('get_current_user', get_current_user ),
    path('shop_id_selfie', shop_id_selfie),
    path('new_shop_owner', new_shop_owner),
    path('verification/get_image', get_image),
    path('verification/document_status', document_status),
    path('verification/get_shop_owner_details', get_shop_owner_details),
    path('verification/get_list_pending', get_list_pending),
    path('verification/approve_or_reject', approve_or_reject)

]
