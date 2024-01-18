from django.urls import path
from .views import *
urlpatterns = [
    path('new_collection', CollectionController.create_collection),
    path('rename_collection', CollectionController.rename_collection),
    path('delete_collection', CollectionController.delete_collection),
    path('get_collections', CollectionController.get_collections),
    path('get_collection_items', CollectionController.get_collection_items),
    path('add_item_to_collection', CollectionController.add_item_to_collection),
    path('remove_item_from_collection', CollectionController.remove_item_from_collection)
]