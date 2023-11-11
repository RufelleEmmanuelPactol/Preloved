from django.db import models

# Create your models here.

class FileType(models.Model):
    extension = models.CharField(max_length=10)
    type = models.CharField(max_length=30)

class StorageBucket(models.Model):
    link = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

class File(models.Model):
    fileTypeID = models.ForeignKey(FileType, on_delete=models.SET_NULL, null=True)
    bucketStorageID = models.ForeignKey(StorageBucket, on_delete=models.SET_NULL, null=True)
    link = models.CharField(max_length=1028)
