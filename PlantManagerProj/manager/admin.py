from django.contrib import admin
from manager.models import Plant

# Register your models here.
class PlantAdmin(admin.ModelAdmin):
    exclude = ('slug',)

admin.site.register(Plant, PlantAdmin)
