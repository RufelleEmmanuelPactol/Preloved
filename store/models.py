from django.db import models
from preloved_auth.models import Location, ShopOwner
# Create your models here.



class Store(models.Model):
    storeID = models.AutoField(primary_key=True)
    locationID = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='stores')
    storeName = models.CharField(max_length=255)
    shopOwnerID = models.ForeignKey(ShopOwner, on_delete=models.CASCADE, related_name='stores')

    def __str__(self):
        return self.storeName

class Item(models.Model):
    itemID = models.AutoField(primary_key=True)
    storeID = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    isFeminine = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    tagID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ItemTag(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('item', 'tag')

    def __str__(self):
        return f"{self.item.name} - {self.tag.name}"


class Slug(models.Model):
    slugID = models.AutoField(primary_key=True)
    slug = models.SlugField(unique=True)
    itemID = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='slugs')

    def __str__(self):
        return self.slug






