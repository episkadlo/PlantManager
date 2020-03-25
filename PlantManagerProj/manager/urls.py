from django.conf.urls import url
from . import views

app_name = 'manager'

urlpatterns = [
    url(r'^$', views.ListPlants, name='list'),
    url(r'newplant/$', views.CreatePlant.as_view(), name='createPlant'),
    url(r'settings/$', views.Settings, name='settings'),
    url(r'editplant/(?P<pk>\d+)/$', views.PlantEdit.as_view(), name='edit_plant'),
    url(r'waterPlants/$', views.waterPlants, name='waterPlants')
]