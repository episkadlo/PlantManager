from datetime import date, timedelta
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


# Create your models here.

User = get_user_model()

class Location(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.CharField(max_length=50)

    
    class Meta:
        verbose_name = _('location')
        verbose_name_plural = _('locations')
        ordering = ['room']
        unique_together = ['owner', 'room']

    def __str__(self):
        return f'{self.owner} : {self.room}'

class Plant(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    name = models.CharField(max_length=30)
    slug = models.SlugField(allow_unicode=True, default="")
    description = models.CharField(max_length=256, blank=True, default="")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='location', blank=True, default="")
    plant_image = models.ImageField(upload_to='media/plant_pics', blank=True)
    last_water = models.DateField(default=date.today)
    water_every = models.PositiveIntegerField(
        default=7,
        editable=True,
        validators=[MinValueValidator(1),
        MaxValueValidator(60)])
    last_fertilize = models.DateField(default=date.today)
    fertilize_every = models.PositiveIntegerField(
        default=30,
        editable=True,
        validators=[MinValueValidator(1),
        MaxValueValidator(60)])

    
    @property
    def next_water(self):
        return self.last_water + timedelta(days=self.water_every)

    @property
    def next_fertilize(self):
        return self.last_fertilize + timedelta(days=self.fertilize_every)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.owner) + '_' + str(self.name))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('manager:list')

    class Meta:
        verbose_name = _('plant')
        verbose_name_plural = _('plants')
        ordering = ['location']
        unique_together = ['owner', 'name']

    def __str__(self):
        return self.name

    

