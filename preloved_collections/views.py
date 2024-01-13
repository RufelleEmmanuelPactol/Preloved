from django.http import JsonResponse
from django.shortcuts import render
from store.views import return_not_auth, return_not_post, return_id_not_found
from .models import *
# Create your views here.


class CollectionController:

    ## Important! Convenience method, do not include in documentation
    @staticmethod
    def get_shop_user(request):
        user = ShopUser.objects.get(userID=request.user)
        if user is None:
            return JsonResponse({'message': 'User is not a shop user'}, status=400)
        return user


    @staticmethod
    def create_collection(request):
        if request.method != 'POST':
            return return_not_post()
        user = CollectionController.get_shop_user(request)
        if not isinstance(user, ShopUser):
            return user
        collection_name = request.POST['collection_name']
        Collection.objects.create(name=collection_name, user=user)
        return JsonResponse({'message': 'success'}, status=201)



    @staticmethod
    def delete_collection(request):
        if not request.user.is_authenticated:
            return return_not_auth()
        if request.method != 'POST':
            return return_not_post()
        user = CollectionController.get_shop_user(request)
        if not isinstance(user, ShopUser):
            return user
        
        collectionID = request.POST.get('collectionID')
        if collectionID is None:
            return JsonResponse({'error': 'Invalid collection ID'}, status=400)
        collection = Collection.objects.get(id=collectionID)
        if collection is None:
            return JsonResponse({'error': 'Invalid collection ID'}, status=400)
        Collection.objects.get(user=user, collection=collection).delete()
        return JsonResponse({'success': True}, status=200)


    @staticmethod
    def get_collections(request):
        if not request.user.is_authenticated:
            return return_not_auth()
        user = CollectionController.get_shop_user(request)
        if not isinstance(user, ShopUser):
            return user
        collections = Collection.objects.filter(user=user, is_deleted=0)
        collection_list = []
        for collection in collections:
            instance = {}
            instance['id'] = collection.id
            instance['name'] = collection.name
            instance['created_at'] = collection.created_at
            collection_list.append(instance)
        return JsonResponse({'collections': collection_list}, status=200)

    @staticmethod
    def get_collection_items(request):
        if not request.user.is_authenticated:
            return return_not_auth()
        user = CollectionController.get_shop_user(request)
        if not isinstance(user, ShopUser):
            return user

        collectionID = request.GET.get('collection_id')
        if collectionID is None:
            return JsonResponse({'error': 'Invalid collection ID'}, status=400)

        collection = Collection.objects.get(id=collectionID)

        set = CollectionItemUser.objects.filter(collection=collection, is_deleted=False)

        collection_list = []

        for item in set:
            collection_list.append(item.item.itemID)
        returning_value = {'collectionID': collectionID, 'collectionName': collection.name, 'itemIDs': collection_list}
        return JsonResponse(returning_value, status=200)


    @staticmethod
    def add_item_to_collection(request):
        if not request.user.is_authenticated:
            return return_not_auth()
        if request.method != 'POST':
            return return_not_post()
        user = CollectionController.get_shop_user(request)
        if not isinstance(user, ShopUser):
            return user

        collectionID = request.POST.get('collectionID')
        if collectionID is None:
            return JsonResponse({'error': 'Invalid collection ID'}, status=400)
        collection = Collection.objects.get(id=collectionID)
        item = request.POST.get('itemID')
        item = Item.objects.get(itemID=item)
        if item is None:
            return JsonResponse({'error': 'Invalid item ID'}, status=400)
        CollectionItemUser.objects.create(user=user, collection=collection, item=item)
        return JsonResponse({'success': True}, status=200)


    @staticmethod
    def remove_item_from_collection(request):
        if not request.user.is_authenticated:
            return return_not_auth()
        if request.method != 'POST':
            return return_not_post()
        user = CollectionController.get_shop_user(request)
        if not isinstance(user, ShopUser):
            return user

        collectionID = request.POST.get('collectionID')
        if collectionID is None:
            return JsonResponse({'error': 'Invalid collection ID'}, status=400)
        collection = Collection.objects.get(id=collectionID)
        item = request.POST.get('itemID')
        item = Item.objects.get(itemID=item)
        if item is None:
            return JsonResponse({'error': 'Invalid item ID'}, status=400)
        CollectionItemUser.objects.get(user=user, collection=collection, item=item).delete()
        return JsonResponse({'success': True}, status=200)

    @staticmethod
    def rename_collection(request):
        if not request.user.is_authenticated:
            return return_not_auth()
        if request.method != 'POST':
            return return_not_post()
        user = CollectionController.get_shop_user(request)
        if not isinstance(user, ShopUser):
            return user

        collectionID = request.POST.get('collectionID')
        if collectionID is None:
            return JsonResponse({'error': 'Invalid collection ID'}, status=400)

        # get the name
        new_name = request.POST.get('new_name')
        if new_name is None:
            return JsonResponse({'error': ''
                                          'Invalid new name'}, status=400)

        collection = Collection.objects.get(id=collectionID)
        collection.name = new_name
        collection.save()
        return JsonResponse({'success': True}, status=200)



