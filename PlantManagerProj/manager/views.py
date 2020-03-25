from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from datetime import date

from .models import Plant, Location
from .forms import PlantCreateForm
from django.forms import modelformset_factory


# Create your views here.

class DetailPlant(LoginRequiredMixin, DetailView):
    model = Plant

# class ListPlants(LoginRequiredMixin, ListView):
#     model = Plant
#     #paginate_by = 15
#     template_name = 'manager/list_plants.html'

#     def get_queryset(self):
#         return Plant.objects.filter(owner=self.request.user)

def ListPlants(request):
    users_plants = Plant.objects.filter(owner=request.user)
    return render(request, 'manager/list_plants.html', {'users_plants':users_plants})

def waterPlants(request):
    #print(form_plants)
    pk_list=request.POST.getlist('water_me')
    plants_to_water = Plant.objects.filter(pk__in=pk_list)
    #print(plants_to_water)
    for temp_pk in pk_list:
        temp_plant = Plant.objects.get(pk=temp_pk)
        temp_plant.last_water = date.today()
        temp_plant.save()
    return HttpResponseRedirect(reverse('manager:list'))

class CreatePlant(LoginRequiredMixin, CreateView):
    template_name = 'manager/createPlant.html'
    model = Plant
    form_class = PlantCreateForm
    # fields = ('name', 
    #         'description',
    #         'location', 
    #         'plant_image', 
    #         'last_water', 
    #         'water_every')

    def get_form_kwargs(self):
        kwargs = super(CreatePlant, self).get_form_kwargs()
        kwargs.update({'user' : self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)



def Settings(request):

    current_locations = Location.objects.filter(owner=request.user)

    testFormSet = modelformset_factory(Location, fields=('room',), extra=1)

    if request.method == 'POST':
            formset = testFormSet(request.POST, queryset=Location.objects.none())
            if formset.is_valid():
                new_instances = formset.save(commit=False)
                for object in formset.deleted_objects:
                    object.delete()
                for new_instance in new_instances:
                    new_instance.owner = request.user
                    new_instance.save()

    formset = testFormSet(queryset=Location.objects.none())

    return render(request, 'manager/settings.html', {"formset" : formset, "current_locations" : current_locations})



class PlantEdit(LoginRequiredMixin, UpdateView):
    fields = ('name', 
            'description',
            'location', 
            'plant_image', 
            'last_water', 
            'water_every')
    model = Plant
    template_name = 'manager/edit_plant.html'
