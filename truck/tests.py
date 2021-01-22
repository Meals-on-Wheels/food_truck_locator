from django.test import TestCase

from django.contrib.auth.models import User
from django.test import TestCase
from .models import TruckInstance, MenuItem, 

class TruckInstanceTestCase(TestCase):
    def setUp(self):
        self.menuItem = MenuItem.objects.create(item="Hummus", description="drizzle with olive oil", cost=3.99)
        self.truckInstance = TruckInstance.objects.create(owner = "Alex", name = "Alex's Hot Dogs", menu = menuItem, location = "5301 156thst. SE, Bothell, WA 98012", contact = "4253455395", album = models.ManyToManyField(ImageLink, blank=True)
)

    def test_menu_item_exists(self):
        self.assertIsNotNone(self.menuItem)

    def test_truck_exists(self):
        self.assertIsNotNone(self.truckInstance)

    

    

    
