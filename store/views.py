from django.http import JsonResponse
from django.shortcuts import render
from .models import Item, Store, Tag, Slug, ItemTag
from preloved_auth.models import ShopOwner, Location
from storage.views import StorageWorker

storage_worker = StorageWorker()

def return_not_post():
    return JsonResponse({'error': 'not a post-type request'}, status=400)


def thumbnailify(id):
    set = Slug.objects.filter(itemID=id, isThumbnail=1)
    if set is None:
        return 1
    return 0


# Create your views here.

def return_id_not_found():
    return JsonResponse({'error': 'Specified id not found.'}, status=400)


def return_not_auth():
    # raise Exception("User not authenticated")
    return JsonResponse({'error': 'user not authenticated'}, status=400)


class ShopController:

    @staticmethod
    def get_store_owner(request):
        try:
            return ShopOwner.objects.filter(userID=request.user).first()
        except Exception as e:
            return None

    @staticmethod
    def get_store(request):
        try:
            owner = self.get_store_owner(request)

            return Store.objects.filter(shopOwnerID=owner).first()
        except Exception as e:
            return None

    def new_store(self, request):
        if not request.user.is_authenticated:
            if not request.user.is_staff:
                return return_not_auth()
        ## IMPLEMENT!

    def get_all_items(self, request):
        if not request.user.is_authenticated:
            if not request.user.is_staff:
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
        if request.method != 'POST':
            return return_not_post()
        POST = request.POST
        store = self.get_store(request)
        description = POST.get('description')
        style = int(POST.get('isFeminine'))
        name = POST.get('name')
        tagID = int(POST.get('tagID'))
        price = float(POST.get('price'))

        t = Tag.objects.filter(id=tagID)




        if store is None:
            return JsonResponse({'error': 'Shop has no store'}, status=400)
        item = Item(storeID=store, description=description, isFeminine=style, name=name, price=price)
        item.save()
        ItemTag(tag=t, item=item).save()
        return JsonResponse({'response': 'Ok!', 'generatedID': item.itemID})

    def get_all_tags(self, request):
        tags = {}
        for x in Tag.objects.all():
            tags[x.name] = x.tagID
        return JsonResponse(tags)

    def create_new_shop(self, request):
        if not request.user.is_authenticated:
            if not request.user.is_staff:
                return return_not_auth()
        if request.method != 'POST':
            return return_not_post()
        address = request.POST.get('address')
        location = Location(address_plain=address)
        location.save()
        name = request.POST.get('name')
        owner = self.get_store_owner(request)
        if owner is None:
            return JsonResponse({'error': 'User is not a shop owner'}, status=400)
        store = Store(shopOwnerID=owner, locationID=location, storeName=name)
        store.save()
        return JsonResponse({'response': 'Ok!', 'storeID': store.storeID})

    @staticmethod
    def attach_image_to_item(request):
        if request.method != 'POST':
            return return_not_post()


        imgStream = request.FILES.get('img')
        imgID = int(request.POST.get('id'))
        item = Item.objects.filter(itemID=imgID).first()
        if item is None:
            return return_id_not_found()
        bld = ""
        for i in imgStream.name:
            if i != " ":
                bld += i
        imgStream.name = bld
        slugString = storage_worker.upload_in_namespace(request, imgStream, namespace='item_images/', slug=imgStream.name)
        slug = Slug(slug=slugString, itemID=item, isThumbnail=thumbnailify(imgID))
        slug.save()

        return JsonResponse({'response' : 'Ok!', 'slug' : slugString})

    @staticmethod
    def get_item_details(request):
        if not request.user.is_authenticated:
            return return_not_auth()

        response = {}
        id = int(request.GET.get('id'))
        retrieved = Item.objects.filter(itemID=id).first()
        if retrieved is None:
            return return_id_not_found()
        response['itemID'] = retrieved.itemID
        response['storeID'] = retrieved.storeID.storeID
        response['name'] = retrieved.name
        response['description'] = retrieved.description
        response['isFeminine'] = bool(retrieved.isFeminine)
        return JsonResponse(response)


    @staticmethod
    def get_balance(request):
        if not request.user.is_authenticated:
            return return_not_auth()
        ownerID = request.GET.get('id')
        s = ShopOwner.objects.filter(id=ownerID).first()
        if s is None:
            return_id_not_found()
        return JsonResponse({'balance': s.balance})

    @staticmethod
    def add_balance(request):
        if not request.user.is_authenticated:
            return return_not_auth()
        if not request.user.is_superuser:
            return return_not_auth()
        id = int(request.POST['id'])
        owner = ShopOwner.objects.filter(id=id).first()
        if owner is None:
            return return_id_not_found()
        owner.balance = float(request.POST['increase'])
        owner.save()
        return JsonResponse({'response' : 'OK!', 'balance': owner.balance})





shopController = ShopController()


def add_item(request):
    return shopController.add_item(request)


def get_all_tags(request):
    return shopController.get_all_tags(request)


def create_new_shop(request):
    return shopController.create_new_shop(request)


