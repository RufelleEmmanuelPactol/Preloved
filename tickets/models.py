from django.db import models
from django.utils import timezone

from store.models import Store, Item
from preloved_auth.models import ShopUser
from django.db import models

class Status(models.Model):
    statusID = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=255)
    level = models.IntegerField()

    def __str__(self):
        return self.status_name

class Ticket(models.Model):
    ticketID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(ShopUser, on_delete=models.CASCADE, related_name='tickets', default=0)
    storeID = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='tickets')
    itemID = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='tickets')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='tickets', default=1)
    created = models.DateTimeField(default=timezone.now)  # default is now
    expected_seller_fulfillment = models.DateField(null=True)
    expected_buyer_fulfillment = models.DateField(null=True)


    def __str__(self):
        return f"Ticket {self.ticketID} - Status: {self.status}"
