from django.urls import include, path
from .views import Storage
urlpatterns = [
    path('q', Storage.as_view(), name='storage')
]