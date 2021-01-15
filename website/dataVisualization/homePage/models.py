from __future__ import unicode_literals

from django.db import models
from multiselectfield import MultiSelectField
from homePage.storage import OverwriteStorage

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
    projectName = models.CharField(max_length=30)
    mentorName = models.CharField(max_length=30)
    school = models.CharField(max_length=30)
    startDate = models.DateField()
    endDate = models.DateField()
    podUseType = MultiSelectField(choices=USETYPE,max_choices=4,max_length=4)
    pollutantOfInterest = MultiSelectField(choices=POLLUTANTOFINTEREST,max_choices=4,max_length=4)
    podUseReason = models.TextField()
    userName = models.CharField(max_length=30)
    docfile = models.FileField(upload_to='')
    averageMinuteFile = models.FileField(upload_to='')
    averageDayFile = models.FileField(upload_to='')
    averageHourFile = models.FileField(upload_to='')
    

