from django.test import TestCase

from django.contrib.auth.models import User
from django.test import TestCase
from .models import TruckInstance, MenuItem
class TruckInstanceTestCase(TestCase):
    def setUp(self):
        self.menuItem = MenuItem.objects.create(item="Hummus", description="drizzle with olive oil", cost=3.99)
    def test_menu_item_exists(self):
        self.assertIsNotNone(self.menuItem)
