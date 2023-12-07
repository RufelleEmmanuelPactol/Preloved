from django.urls import include, path
from .views import TicketController, PurchaseController
urlpatterns = [
    path('ticket/', TicketController.as_view()),
    path('purchase_item', PurchaseController.purchase_item),
]