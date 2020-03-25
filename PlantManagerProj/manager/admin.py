from django.contrib import admin
from manager.models import Plant, Location

# Register your models here.
class PlantAdmin(admin.ModelAdmin):
    exclude = ('slug',)

admin.site.register(Plant, PlantAdmin)
admin.site.register(Location)
