from datetime import date, timedelta
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

User = get_user_model()

class Plant(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True, default="")
    description = models.CharField(max_length=256, blank=True, default="")
    plant_image = models.ImageField(upload_to='plant_pics', blank=True)
    last_water = models.DateField(default=date.today)
    water_every = models.PositiveIntegerField(
        default=7,
        editable=True,
        validators=[MinValueValidator(1),
        MaxValueValidator(60)])


    @property
    def next_water(self):
        return self.last_water + timedelta(days=self.water_every)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('manager:single', kwargs={'user':self.owner.username, 'slug':self.slug})

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
