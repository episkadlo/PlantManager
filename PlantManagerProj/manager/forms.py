from django.forms import ModelForm, modelformset_factory
from .models import Plant, Location

class PlantCreateForm(ModelForm):
    class Meta:
        model=Plant
        exclude = ['slug', 'owner']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(PlantCreateForm,self).__init__(*args, **kwargs)
        self.fields['location'].queryset = Location.objects.filter(owner=user)


