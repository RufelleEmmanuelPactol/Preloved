from django.db import models
from preloved_auth.models import ShopUser
from django.db.models import CASCADE
from store.models import Item


# Create your models here.


class Collection(models.Model):
    name = models.CharField(max_length=256)
    user = models.ForeignKey(ShopUser, on_delete=CASCADE)
    is_deleted = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class CollectionItemUser(models.Model):
    collection = models.ForeignKey(Collection, on_delete=CASCADE)
    user = models.ForeignKey(ShopUser, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Item, on_delete=CASCADE)
    is_deleted = models.IntegerField(default=0)

    class Meta:
        unique_together = ('collection', 'user', 'item')
