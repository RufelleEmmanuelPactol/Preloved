import os

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, FileResponse, HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
# Create your views here.



class StorageWorker:

    def upload_in_namespace(self, request, file, namespace="", slug="", extension=""):
        if not request.user.is_authenticated:
            return None
        if len(slug) == 0:
            slug = file.name
        if request.user.is_authenticated:
            file_path = f"users/{request.user.email}/usercontent/{namespace}{slug}{extension}"
            default_storage.save(file_path, ContentFile(file.read()))
            return file_path

    def get_in_namespace(self, request, filename, namespace=""):
        if request.user.is_authenticated:
            return default_storage.open(f"users/{request.user.email}/usercontent/{namespace}{filename}")


class Storage(View):

    # posts a new resource
    def post(self, request):
        if request.user.is_authenticated:
            email = request.user.email
            path = request.POST['path']
            file = request.FILES['file']
            default_storage.save(f"users/{email}/usercontent/{path}/{file.name}", ContentFile(file.read()))
            return JsonResponse({'status': 'request OK!'})
        else:
            return JsonResponse({'error': 'user is not authenticated', 'user': str(request.user)})




    # Returns a resource given their username

    def get(self, request):


        if request.user.is_authenticated:

            email = request.user.email
            path = request.GET.get('path')


            if path is None:
                return JsonResponse({'error': 'cannot find file'})
            try:
                file = default_storage.open(f"users/{email}/usercontent/{path}")
                response = HttpResponse(file.read(), content_type='application/octet-stream')
                filename = os.path.basename(file.name)
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                file.close()
                return response
            except Exception as e:
                return JsonResponse({'error': str(e), 'path': f"users/{email}/usercontent/{path}"})

        else:
            return JsonResponse({'error': 'cannot find file'})

