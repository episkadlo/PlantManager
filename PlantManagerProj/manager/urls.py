from django.urls import path
from . import views

app_name = 'manager'

urlpatterns = [
    path('', views.ListPlants, name='list'),
    path('newplant/', views.CreatePlant.as_view(), name='createPlant'),
    path('settings/', views.Settings, name='settings'),
    path('waterPlants/', views.waterPlants, name='waterPlants'),
    path('edit/<slug:slug>', views.PlantEdit.as_view(), name='editPlant'),
    path('delete/<slug:slug>', views.PlantDelete.as_view(), name='deletePlant'),
    path('deleteLoc/<int:pk>', views.LocationDelete.as_view(), name='deleteLoc'),
    path('editLoc/<int:pk>', views.LocationEdit.as_view(), name='editLoc')
]