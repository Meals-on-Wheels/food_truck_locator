from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class UserLocation(models.Model):
    user = models.OneToOneField(User, on_delete = models.SET_NULL, null = True)
    lat = models.DecimalField(max_digits=25, decimal_places=22)
    lng = models.DecimalField(max_digits=25, decimal_places=22)
    
    def latlng(self): 
        return f'{self.lat}, {self.lng}'

    def __str__(self):
        return f'{self.lat}, {self.lng}'

class ImageLink(models.Model):
    title = models.CharField(max_length=75, help_text='What is the pictures name.', blank=True)
    link = models.URLField(max_length=250, help_text='Enter the target URL.')

    def __str__(self):
        return f'{self.title}'

class MenuItem(models.Model):
    item = models.CharField(max_length=75, help_text='Enter the name of the dish.')
    description = models.CharField(max_length=450, help_text='Enter a description of the dish.', default='No description given.')
    cost = models.DecimalField(max_digits = 8, decimal_places=2, help_text='Enter the cost of the dish')

    def __str__(self):
        return f'{self.item}'

class TruckInstance(models.Model):

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=75, help_text='Enter the store name.')
    menu = models.ManyToManyField(MenuItem, blank=True)
    location = models.CharField(max_length=75, help_text='Enter the current location.', default='Closed')
    contact = models.CharField(max_length=18, help_text='Enter a working number for the truck.', blank=True)
    album = models.ManyToManyField(ImageLink, blank=True)

    class Meta:
        ordering = ['name', 'owner', 'location']

    def __str__(self):
        return f'{self.name}'

class OrderItem(models.Model):

    item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return 'item: {} x {}'.format(self.item.item, self.quantity)

    def item_cost(self):
        return self.item.cost*self.quantity

class OrderInstance(models.Model):

    poster = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    truck = models.ForeignKey(TruckInstance, on_delete=models.SET_NULL, null=True)
    inventory = models.ManyToManyField(OrderItem, blank=True)
    prepared = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.truck.name}'

    def display_inventory(self):
        return ', '.join([f'{item.quantity} x {item.item.item}' for item in self.inventory.all()])

    def calculate_total(self):
        return sum([item.item_cost() for item in self.inventory.all()])

    def list_inventory(self):
        checkout_vals = [f'{item.item.item} x {item.quantity}: {item.quantity*item.item.cost}' for item in self.inventory.all()]
        checkout_vals.append(f'total: {self.calculate_total()}')
        return checkout_vals

    def order(self):
        return 'order: {} | vendor: {} | customer: {}'.format(self.id, self.truck.name, self.poster.username)

    display_inventory.short_description = 'items'