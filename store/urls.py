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
    path('codegen', ShopController.codegen),
    path('stores', ShopController.get_stores),
    path('item_images', ShopController.get_item_images),
    path('attach_tag_to_item', ShopController.attach_tag_to_item),
    path('get_shop_details', ShopController.get_shop_details),
    path('get_shop_items', ShopController.get_shop_items)

]