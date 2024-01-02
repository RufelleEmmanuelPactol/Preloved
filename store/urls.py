from django.urls import path
from .views import add_item, get_all_tags, create_new_shop, ShopController

urlpatterns = [
    path('add_item', add_item),
    path('get_all_tags', get_all_tags),
    path('create_new_shop', create_new_shop),
    path('add_img_item', ShopController.attach_image_to_item),
    path('get_item_details', ShopController.get_item_details),
    path('get_balance', ShopController.get_balance),
    path('add_balance', ShopController.add_balance),
    path('redeem_voucher', ShopController.redeem_voucher),

]