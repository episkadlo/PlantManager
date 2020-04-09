from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from datetime import date, timedelta
from django.db.models import F

from .models import Plant, Location
from .forms import PlantCreateForm, PlantEditForm
from django.forms import modelformset_factory, ValidationError


# Create your views here.

class DetailPlant(LoginRequiredMixin, DetailView):
    model = Plant

# class ListPlants(LoginRequiredMixin, ListView):
#     model = Plant
#     #paginate_by = 15
#     template_name = 'manager/list_plants.html'

#     def get_queryset(self):
#         return Plant.objects.filter(owner=self.request.user)

@login_required
def ListPlants(request):
    users_plants = Plant.objects.filter(owner=request.user)

    takeCareOf_id = [x.id for x in Plant.objects.filter(owner=request.user) if x.next_water < date.today() or x.next_fertilize < date.today() ]
    takeCareOf = Plant.objects.filter(id__in=takeCareOf_id)
    
    upToDate_id = [x.id for x in Plant.objects.filter(owner=request.user) if x.next_water >= date.today() and x.next_fertilize >= date.today()]
    upToDate = Plant.objects.filter(id__in=upToDate_id)

    return render(request, 'manager/list_plants.html', {'users_plants':users_plants, 'upToDate':upToDate, 'takeCareOf':takeCareOf})

def waterPlants(request):
    #print(form_plants)
    pk_water=request.POST.getlist('water_me')
    plants_to_water = Plant.objects.filter(pk__in=pk_water)
    #print(plants_to_water)
    for temp_pk in pk_water:
        temp_plant = Plant.objects.get(pk=temp_pk)
        temp_plant.last_water = date.today()
        temp_plant.save()

    pk_fertilize=request.POST.getlist('fertilize_me')
    plants_to_fertilize = Plant.objects.filter(pk__in=pk_fertilize)
    for temp_pk in pk_fertilize:
        temp_plant = Plant.objects.get(pk=temp_pk)
        temp_plant.last_fertilize = date.today()
        temp_plant.save()
        
    return HttpResponseRedirect(reverse('manager:list'))

class CreatePlant(LoginRequiredMixin, CreateView):
    template_name = 'manager/createPlant.html'
    model = Plant
    form_class = PlantCreateForm

    def get_form_kwargs(self):
        kwargs = super(CreatePlant, self).get_form_kwargs()
        kwargs.update({'user' : self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


@login_required
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
                    if Location.objects.filter(room = new_instance, owner=request.user).exists():
                        raise ValidationError("This location already exists")
                    else:
                        new_instance.owner = request.user
                        new_instance.save()

    formset = testFormSet(queryset=Location.objects.none())

    return render(request, 'manager/settings.html', {"formset" : formset, "current_locations" : current_locations})


class PlantEdit(LoginRequiredMixin, UpdateView):

    model = Plant
    template_name = 'manager/edit_plant.html'
    success_url = ''
    form_class = PlantEditForm


    def get_object(self, *args, **kwargs):
        edited_plant = get_object_or_404(Plant, slug=self.kwargs['slug'])
        print(edited_plant)
        return edited_plant

    def get_form_kwargs(self):
        kwargs = super(PlantEdit, self).get_form_kwargs()
        kwargs.update({'user' : self.request.user})
        return kwargs

class PlantDelete(LoginRequiredMixin, DeleteView):
    model = Plant
    template_name = 'manager/delete_plant.html'
    success_url = reverse_lazy('manager:list')


class LocationDelete(LoginRequiredMixin, DeleteView):
    model = Location
    template_name = 'manager/delete_location.html'
    success_url = reverse_lazy('manager:settings')



class LocationEdit(LoginRequiredMixin, UpdateView):

    model = Location
    fields = ['room',]
    template_name = 'manager/edit_location.html'
    success_url = reverse_lazy('manager:settings')
