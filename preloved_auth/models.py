from django.db import models
from django.contrib.auth.models import User
from storage.models import File
# Create your models here.

class Location(models.Model):
    latitude = models.DecimalField(decimal_places=7, max_digits=8)
    longitude = models.DecimalField(decimal_places=7, max_digits=8)
    name = models.CharField(max_length=256)

class ShopUser(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=20)
    is_feminine = models.IntegerField()
    locationID = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)

class Store(models.Model):
    locationID = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=256)


class ShopOwner(models.Model):
    userID = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    storeID = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True)
    phoneNumber = models.CharField(max_length=20)
    imageID1 = models.ForeignKey(File, on_delete=models.SET_NULL, null=True,  related_name='image1_shopowners')
    imageID2 = models.ForeignKey(File, on_delete=models.SET_NULL, null=True,  related_name='image2_shopowners')

    class Meta:
        unique_together = ('imageID1', 'imageID2')



