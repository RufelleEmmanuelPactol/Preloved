from django.http import JsonResponse
from django.shortcuts import render

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
            for i in range(20):
                items.append(item.pop())
        except IndexError:
            pass
        return JsonResponse({'items': items})

    @staticmethod
    def generate_iterative_homepage():
        items = Item.objects.filter(isTaken=0).order_by('?')
        item_list = []
        for item in items:
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
        return item_list

    @staticmethod
    def generate_link(slug):
        return preloved_secrets.STORAGE + slug



