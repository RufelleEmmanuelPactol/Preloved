# Create your views here.
import secrets
import string
import os
from django.views.decorators.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse

from .models import ShopUser, ShopOwner, Location, ShopVerification, Staff
from django.core.files.storage import default_storage as storage
from django.core.files.base import ContentFile
from datetime import datetime
from storage.views import StorageWorker

storage_worker = StorageWorker()


def get_file_extension(file_object):
    # Get the file name from the file object
    file_name = os.path.basename(file_object.name)

    # Split the file name into the base name and extension
    _, extension = os.path.splitext(file_name)

    return extension


class LoginController:

    def loginAPI(self, request):
        result = assert_post(request)
        if result:
            return result
        u = authenticate(username=request.POST['email'], password=request.POST['password'])
        if u is not None:
            login(request, u)
            value = {}
            value['id'] = request.user.id
            value['first name'] = request.user.first_name
            value['last name'] = request.user.last_name
            value['email'] = request.user.email
            s = ShopOwner.objects.filter(userID=request.user).first()
            if s is None:
                value['user_type'] = 'Shop User'
                value['user_type_int'] = 0
            else:
                staff = Staff.objects.filter(uID=request.user).first()
                if staff is not None:
                    value['user_type'] = 'Verification Officer'
                    value['user_type_int'] = 2
                else:
                    value['user_type'] = 'Shop Owner'
                    value['user_type_int'] = 1
            return JsonResponse(value)
        return JsonResponse({'error': 'Invalid credentials'}, status=400)

    def logoutAPI(self, request):
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({'status': 'OK!'})
        return JsonResponse({'error': 'user not authenticated'}, status=400)

    def is_logged_in(self, request):
        if request.user.is_authenticated:
            return JsonResponse({'response': True})
        return JsonResponse({'response': False})


controller = LoginController()

def return_not_post():
    return JsonResponse({'error': 'not a post-type request'}, status=400)

def return_not_auth():
    return JsonResponse({'error': 'user not authenticated'}, status=400)


def generate_id(length=12):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string


def assert_post(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'not a post-type request'}, status=400)


class SignUpController:

    def new_shop_user(self, request):
        result = assert_post(request)
        if result:
            return result
        try:
            email = request.POST['email']
            password = request.POST['password']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            phone_no = request.POST['phone_no']
            isFeminine = int(request.POST['isFeminine'])
            locationID = None
            u = User.objects.create_user(username=email, email=email, password=password, first_name=first_name,
                                         last_name=last_name, is_staff=1)
            ShopUser.objects.create(userID=u, phone_no=phone_no, locationID=locationID, is_feminine=isFeminine)

        except KeyError as key_error:
            return JsonResponse({'error': f'Missing required parameter: {key_error}'}, status=400)

        except Exception as ex:
            msg = f'Error: {str(ex)}'
            print('Error:', msg)
            return JsonResponse({'error': msg})

        storage.save(f'users/{email}/init.txt', ContentFile(f"autogenerated::{str(datetime.now())}".encode('utf-8')))
        return JsonResponse({'status': 'OK!'})

    def new_shop_owner(self, request):
        result = assert_post(request)
        if result:
            return result
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_no = request.POST['phone_no']
        address_line = request.POST['address']
        u = User.objects.create_user(email=email, username=email, password=password,
                                     first_name=first_name, last_name=last_name)
        l = Location.objects.create(address_plain=address_line)
        s = ShopOwner.objects.create(userID=u, phoneNumber=phone_no, locationID=l)
        ShopVerification(shopOwnerID=s).save()
        return JsonResponse({'response': 'Ok!'})

    def shop_id_one(self, request):
        result = assert_post(request)
        if result:
            return result
        if request.user.is_authenticated:
            shop_owner = ShopOwner.objects.filter(userID=request.user).first()
            slugs = ShopVerification.objects.filter(shopOwnerID=shop_owner).first()
            file = request.FILES['file']
            file_path = storage_worker.upload_in_namespace(request, file, namespace='verification/', slug=file.name)

            if file_path is None:
                return return_not_auth()
            slugs.idSlug1 = file_path
            slugs.save()
            return JsonResponse({'response': 'Ok!'})
        return return_not_auth()

    def shop_id_two(self, request):
        result = assert_post(request)
        if result:
            return result
        if request.user.is_authenticated:
            shop_owner = ShopOwner.objects.filter(userID=request.user).first()
            slugs = ShopVerification.objects.filter(shopOwnerID=shop_owner).first()
            file = request.FILES['file']
            file_path = storage_worker.upload_in_namespace(request, file, namespace='verification/', slug=file.name)
            if file_path is not None:
                return return_not_auth()
            slugs.idSlug2 = file_path
            slugs.save()
            return JsonResponse({'response': 'Ok!'})
        return return_not_auth()

    def shop_id_selfie(self, request):
        result = assert_post(request)
        if result:
            return result
        if request.user.is_authenticated:
            shop_owner = ShopOwner.objects.filter(userID=request.user).first()
            slugs = ShopVerification.objects.filter(shopOwnerID=shop_owner).first()
            file = request.FILES['file']
            file_path = storage_worker.upload_in_namespace(request, file, namespace='verification/', slug=file.name)
            if file_path is not None:
                return return_not_auth()
            slugs.selfieSlug = file_path
            slugs.save()
            return JsonResponse({'response': 'Ok!'})
        return return_not_auth()


class VerificationController:

    def document_status(self, request):
        if not request.user.is_authenticated:
            if Staff.objects.filter(uID=request.user.id) is None:
                return return_not_auth()

            # Retrieve the 'id' from the GET request parameters
        id = request.GET.get('id')

        response = {}
        owner = ShopVerification.objects.filter(shopOwnerID=id).first()

        if not owner:
            response['status'] = 'not found'
        elif owner.idSlug1 is None or owner.idSlug2 is None or owner.selfieSlug is None:
            response['status'] = 'incomplete'
        elif owner.idSlug1 is None:
            response['status'] = 'id 1 is missing'
        elif owner.idSlug2 is None:
            response['status'] = 'id 2 is missing'
        elif owner.selfieSlug is None:
            response['status'] = 'selfie is missing'
        else:
            response['status'] = 'complete'

        return JsonResponse(response)

    def get_image(self, request):
        if not request.user.is_authenticated:
            if Staff.objects.filter(uID=request.user.id) is None:
                return return_not_auth()

        # Get parameters from GET request
        id = request.GET.get('id')
        resource_type = request.GET.get('resource_type')

        if id is None or resource_type is None:
            raise Exception(
                f"Cannot find missing resource type and id where id is {id} and resource type {resource_type}")

        # Retrieve the owner object based on the id
        owner = ShopVerification.objects.filter(shopOwnerID=id).first()

        if not owner:
            raise Exception("Owner of image not found")

        # Determine the image slug based on the resource_type
        if resource_type == "id1":
            image_slug = owner.idSlug1
        elif resource_type == "id2":
            image_slug = owner.idSlug2
        elif resource_type == "selfie":
            image_slug = owner.selfieSlug
        else:
            raise Exception("Cannot find resource type")

        # Assuming img is a binary image file
        img = storage_worker.get_absolute(request, image_slug)

        if img:
            response = HttpResponse(img, content_type='image/png')  # Adjust content type based on the image format
            response['Content-Disposition'] = f'inline; filename={image_slug}.png'  # Set a filename for the image
            return response
        else:
            # Handle the case when the image is not found
            raise Exception("Cannot find image")

    def get_shop_owner_details(self, request):
        if not request.user.is_authenticated:
            if Staff.objects.filter(uID=request.user.id) is None:
                return return_not_auth()
        id = request.GET.get('id')
        user = None
        shop_owner = None
        try:
            shop_owner = ShopOwner.objects.filter(id=id).first()
            user = User.objects.filter(id=shop_owner.userID_id).first()
        except Exception as e:
            return JsonResponse({'error': 'Cannot find queried user.'}, status=400)
        shop_details = {}
        shop_details['isVerified'] = shop_owner.isVerified
        shop_details['email'] = user.email
        shop_details['first_name'] = user.first_name
        shop_details['last_name'] = user.last_name
        return JsonResponse(shop_details)

    def get_list_pending(self, request):
        if not request.user.is_authenticated:
            if Staff.objects.filter(uID=request.user.id) is None:
                return return_not_auth()
        to_verify = []
        for user in ShopVerification.objects.filter(status=0):
            to_verify.append(user.id)
        return JsonResponse(to_verify)

    def approve_or_reject(self, request):
        if request.method != 'POST':
            return return_not_post()
        if not request.user.is_authenticated:
            if Staff.objects.filter(uID=request.user.id) is None:
                return return_not_auth()
        id = request.POST['id']
        status = int(request.POST['updated_status'])
        try:
            obj = ShopVerification.objects.filter(shopOwnerID=id).first()
            obj.status = status
            obj.save()
            return JsonResponse({'response': 'Ok!'})
        except Exception as e:
            return JsonResponse({'error': 'Invalid Shop Owner ID.'}, status=400)


    def get_current_user(self, request):
        try:
            if not request.user.is_authenticated:
                return return_not_auth()

            value = {}
            value['id'] = request.user.id
            value['first name'] = request.user.first_name
            value['last name'] = request.user.last_name
            value['email'] = request.user.email
            s = ShopOwner.objects.filter(userID=request.user).first()
            if s is None:
                value['user_type'] = 'Shop User'
                value['user_type_int'] = 0
            else:
                staff = Staff.objects.filter(uID=request.user).first()
                if staff is not None:
                    value['user_type'] = 'Verification Officer'
                    value['user_type_int'] = 2
                else:
                    value['user_type'] = 'Shop Owner'
                    value['user_type_int'] = 1



            return JsonResponse(value)

        except Exception as e:
            return JsonResponse({'error': str(e)})


verificationController = VerificationController()
signUpController = SignUpController()


## DOCUMENTATION STARTS HERE
## Following format:
## Endpoint Name
## Endpoint URL
## Endpoint METHOD (post, get)


def shop_id_one(request):
    return signUpController.shop_id_one(request)


def shop_id_two(request):
    return signUpController.shop_id_two(request)


def shop_id_selfie(request):
    return signUpController.shop_id_selfie(request)


def new_shop_user(request):
    return signUpController.new_shop_user(request)


def new_shop_owner(request):
    return signUpController.new_shop_owner(request)


def csrf_token(request):
    # Get the CSRF token using Django's get_token function
    csrf_token_value = get_token(request)

    # Return the CSRF token in a JSON response
    return JsonResponse({'csrf_token': csrf_token_value})


def loginAPI(request):
    return controller.loginAPI(request)


def logout_attempt(request):
    return controller.logoutAPI(request)


def is_logged_in(request):
    return controller.is_logged_in(request)


def get_image(request):
    return verificationController.get_image(request)


def document_status(request):
    return verificationController.document_status(request)


def get_shop_owner_details(request):
    return verificationController.get_shop_owner_details(request)


def get_list_pending(request):
    return verificationController.get_list_pending(request)


def approve_or_reject(request):
    return verificationController.approve_or_reject(request)



def get_current_user(request):
    return verificationController.get_current_user(request)
