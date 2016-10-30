from __future__ import unicode_literals

from django.db import models
from multiselectfield import MultiSelectField


USETYPE = ((1, 'Ambient Monitoring'),
           (2, 'Indoor'),
           (3, 'Mobile'),
           (4, 'Experiment'))

POLLUTANTOFINTEREST = ((1, 'VOC1'),
                       (2, 'VOC2'),
                       (3, 'O3'),
                       (4, 'CO2'))

class Document(models.Model):
    podId = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    startDate = models.DateField()
    endDate = models.DateField()
    podUseType = MultiSelectField(choices=USETYPE,max_choices=4,max_length=4)
    pollutantOfInterest = MultiSelectField(choices=POLLUTANTOFINTEREST,max_choices=4,max_length=4)
    podUseReason = models.TextField()
    docfile = models.FileField(upload_to='')