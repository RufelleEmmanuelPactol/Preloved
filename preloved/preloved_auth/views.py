from django.shortcuts import render
from django.views import View
# Create your views here.
import secrets
import string
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import ShopUser


def generate_id(length=12):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string

def new_shop_user(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'not a post-type request'})
    try:
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_no = request.POST['phone_no']
        isFeminine = request.POST['isFeminine']
        locationID = None
        u = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
        ShopUser.objects.create(userID=u.id, phone_no=phone_no, locationID=locationID)
    except Exception as ex:
        msg = str(ex)
        return JsonResponse({'error': msg})
    return JsonResponse({'status': 'OK!'})



