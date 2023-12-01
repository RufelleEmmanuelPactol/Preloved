from django.contrib import admin

from django.urls import path, include
from .views import new_shop_user, csrf_token, loginAPI, logout_attempt, is_logged_in, shop_id_selfie, shop_id_two, shop_id_one, new_shop_owner, get_image, document_status

urlpatterns = [
    path('new_shop_user/', new_shop_user),
    path('csrf_token/', csrf_token),
    path('login/', loginAPI),
    path('logout/', logout_attempt),
    path('is_authenticated/', is_logged_in),
    path('shop_id_one', shop_id_one),
    path('shop_id_two', shop_id_two),
    path('shop_id_selfie', shop_id_selfie),
    path('new_shop_owner/', new_shop_owner),
    path('get_image/', get_image),
    path('document_status/', document_status)

]
