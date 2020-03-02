from django.db import models
from datetime import date

# Create your models here.

class Plants(models.Model):
    name = models.CharField(max_length=30, unique = True)
    description = models.CharField(max_length=256)
    #plant_image = models.ImageField(upload_to = 'plant_pics', blank=True)
    last_water = models.DateField(default=date.today)
    next_water = models.DateField(default=date.today)
    water_every = models.PositiveIntegerField(default=7)

    def __str__(self):
        return self.name
