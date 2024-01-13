from django.http import JsonResponse
from django.shortcuts import render
from .models import *
# Create your views here.

from preloved_auth.models import *
from store.models import *
from store.views import return_not_auth, return_not_post, return_id_not_found
from preloved import preloved_secrets

class HomePageController:

    @staticmethod
    def homepage(request):
        if not request.user.is_authenticated:
            return return_not_auth()
        if request.session.get('items') is None:
            request.session['items'] = []
        if len(request.session.get('items')) == 0:
            request.session['items'] = HomePageController.generate_iterative_homepage()
        item: list = request.session['items']
        items = []
        try:
            for i in range(50):
                items.append(item.pop())
        except IndexError:
            pass
        return JsonResponse({'items': items})

    @staticmethod
    def generate_iterative_homepage(past=None):
        items = Item.objects.filter(isTaken=0).order_by('?')
        item_list = []
        if past is not None:
            item_list += past
        for item in items:
            if item.storeID.shopOwnerID.balance == 0:
                continue
            map = {}
            map['item_id'] = item.itemID
            map['item_name'] = item.name
            map['item_description'] = item.description
            map['item_price'] = item.price
            map['size'] = item.size.sizeType
            map['is_feminine'] = item.isFeminine
            map['storeID'] = item.storeID.storeID
            images = []
            map['images'] = images
            image_slugs = Slug.objects.filter(itemID=item, isDeleted=0)
            for slug in image_slugs:
                images.append({'link': HomePageController.generate_link(slug.slug), 'slugID' : slug.slugID})
            item_list.append(map)
        if len(item_list) < 50:
            return HomePageController.generate_iterative_homepage(item_list)
        return item_list

    @staticmethod
    def generate_link(slug):
        return preloved_secrets.STORAGE + slug


    @staticmethod
    def search(request):
        params = request.GET.get('q')
        from django.db import connections
        cursor = connections['default'].cursor()
        cursor.callproc('search', [params])
        results = cursor.fetchall()
        query_result = []
        for result in results:
            query_result.append({
                'itemID': result[0],
                'name': result[1]
            })
        return JsonResponse({'results': query_result})



class CartController:

    @staticmethod
    def add_to_cart(request):
        if not request.user.is_authenticated:
            return return_not_auth()
        if request.method != 'POST':
            return return_not_post()
        item = request.POST.get('itemID')
        Cart(user=request.user, itemID=item).save()
        return JsonResponse({'success': True})

    @staticmethod
    def remove_from_cart(request):
        if not request.user.is_authenticated:
            return return_not_auth()
        if request.method != 'POST':
            return return_not_post()
        item = request.POST.get('itemID')
        item = Cart.objects.filter(user=request.user, itemID=item)
        if item is None:
            return JsonResponse({'success': False})
        item.delete()
        return JsonResponse({'success': True})

    @staticmethod
    def get_cart_items(request):
        if not request.user.is_authenticated:
            return return_not_auth
        cartItems = Cart.objects.filter(user=request.user)
        shoppingCart = []
        for item in cartItems:
            firstItem: Slug = Slug.objects.filter(isDeleted=0, itemID=item.item).first()
            shoppingCart.append({
                'itemID': item.item.itemID,
                'price': item.item.price,
                'storeName': item.item.storeID.storeName,
                'size': item.item.size.sizeType,
                'thumbnail': preloved_secrets.STORAGE + firstItem.slug
            })
        return JsonResponse({'cart':shoppingCart})

