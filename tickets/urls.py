from django.urls import include, path
from .views import TicketController
urlpatterns = [
    path('ticket/', TicketController.as_view())
]