from django.http import JsonResponse
from django.shortcuts import render
from .models import Item, Store
from preloved_auth import ShopOwner



# Create your views here.

def return_id_not_found():
    return JsonResponse({'error': 'Specified id not found.'}, status=400)


def return_not_auth():
    # raise Exception("User not authenticated")
    return JsonResponse({'error': 'user not authenticated'}, status=400)



class ShopController:


    def get_store_owner(self, request):
        try:
            return ShopOwner.objects.filter(userID=request.user).first()
        except Exception as e:
            return None

    def get_store(self, request):
        try:
            owner = self.get_store_owner(request)
            return Store.objects.filter(shopOwnerID=owner).first()
        except Exception as e:
            return None


    def get_all_items(self, request):
        if not request.user.is_authenticated:
            return return_not_auth()
        try:
            id = int(request.GET.get('id'))
            sets = Item.objects.filter(storeID=Store.objects.filter(storeid=id).first())
            items = []
            for item in sets:
                items.append(item.itemID)
            return JsonResponse(items)
        except Exception as e:
            return return_id_not_found()


    def add_item(self, request):
        if not request.user.is_authenticated:
            if not request.user.is_staff:
                return return_not_auth()
        POST = request.POST
        store = self.get_store(request)
        description = POST['description']
        style = int(POST['isFeminine'])
        name = POST['name']
        item = Item(storeID=store, description=description, isFeminine=style, name=name)
        item.save()
        return JsonResponse({'response': 'Ok!', 'generatedID': item.itemID})




shopController = ShopController()
