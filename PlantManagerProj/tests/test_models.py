from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date, timedelta

from manager.models import Plant, Location


class LocationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='12345')
        Location.objects.create(owner=user, room='Living room')


    def test_str(self):
        loc = Location.objects.get(pk=1)
        expected_object_name = f'{loc.owner} : {loc.room}'
        self.assertEquals(expected_object_name, str(loc))

    def test_owner(self):
        loc = Location.objects.get(pk=1)
        test_owner = str(loc.owner)
        self.assertEquals(test_owner, 'testuser')

class PlantModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='12345')
        Location.objects.create(owner=user, room='Living room')
        Plant.objects.create(owner=user, 
                            name='Cactus', 
                            location=Location.objects.get(pk=1), 
                            last_water = date(2020, 1, 15),
                            water_every=5, 
                            last_fertilize = date(2020, 1, 1),
                            fertilize_every=10)
    
    def test_str(self):
        plant = Plant.objects.get(pk=1)
        expected_object_name = "Cactus"
        self.assertEquals(str(plant), expected_object_name)

    def test_next_water(self):
        plant = Plant.objects.get(pk=1)
        exp_date_next_water = plant.last_water + timedelta(days=plant.water_every)
        self.assertEquals(plant.next_water, exp_date_next_water)

    def test_next_fertilize(self):
        plant = Plant.objects.get(pk=1)
        exp_date_next_fertilize = plant.last_fertilize + timedelta(days=plant.fertilize_every)
        self.assertEquals(plant.next_fertilize, exp_date_next_fertilize)
