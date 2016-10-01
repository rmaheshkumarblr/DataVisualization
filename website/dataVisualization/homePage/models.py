from __future__ import unicode_literals

from django.db import models

# Create your models here.
class uploadedFile(models.Model):
    nameOfUploadedFile = models.CharField(max_length=200)
    uploadedDate = models.DateTimeField('Updated Date')

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')