from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Location(models.Model):
    latitude = models.DecimalField(decimal_places=7, max_digits=8, null=True)
    longitude = models.DecimalField(decimal_places=7, max_digits=8, null=True)
    name = models.CharField(max_length=256, null=True)
    address_plain = models.CharField(max_length=1086)

class ShopUser(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=20)
    is_feminine = models.IntegerField()
    locationID = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)



class ShopOwner(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    phoneNumber = models.CharField(max_length=20)
    locationID = models.ForeignKey(Location, on_delete=models.CASCADE)
    isVerified = models.IntegerField(default=0)




class ShopVerification(models.Model):
    shopOwnerID = models.ForeignKey(ShopOwner, on_delete=models.CASCADE)
    idSlug1 = models.CharField(max_length=256)
    idSlug2 = models.CharField(max_length=256)
    selfieSlug = models.CharField(max_length=256)
    status = models.IntegerField(default=0)

    class Meta:
        unique_together = ('idSlug1', 'idSlug2', 'selfieSlug')



class Store(models.Model):
    locationID = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    ownerID = models.ForeignKey(ShopOwner, on_delete=models.CASCADE)


class Staff(models.Model):
    uID = models.ForeignKey(User, on_delete=models.CASCADE)




