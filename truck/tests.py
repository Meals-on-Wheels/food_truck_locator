from django.test import TestCase
from django.contrib.auth.models import User
from django.test import TestCase
from .models import TruckInstance, MenuItem, UserLocation, ImageLink, OrderInstance

class TruckInstanceTestCase(TestCase):
    def setUp(self):
        self.menuItem = MenuItem.objects.create(item="Hummus", description="drizzle with olive oil", cost=3.99)
        self.truckItem =TruckInstance.objects.create( 
            name = "bobs burgers",
            location = "1234 merry ln. Seattle, Wa 98208",
            contact = "555-555-5555"
        )
        self.userLocation = UserLocation.objects.create(
            lat = 47.606209,
            lng = -122.332069
        )
        self.imageLink = ImageLink.objects.create(
            title = "I have a name",
            link = "www.pictureURL.com/image01"
        )
        self.orderInstance = OrderInstance.objects.create(
            truck = self.truckItem,
            inventory = self.menuItem,
            prepared = True
        )

    def test_truck_item_exists(self):
        self.assertIsNotNone(self.truckItem)  

    def test_menu_item_exists(self):
        self.assertIsNotNone(self.menuItem)

    def test_user_location(self):
        self.assertIsNotNone(self.userLocation)
    
    def test_image_link(self):
        self.assertIsNotNone(self.imageLink)

    def test_order_item(self):
        self.assertIsNotNone(self.orderInstance)

    
