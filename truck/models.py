from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class ImageLink(models.Model):
    title = models.CharField(max_length=75, help_text='What is the pictures name.')
    link = models.URLField(max_length=250, help_text='Enter the target URL.')

    def __str__(self):
        return f'{self.title}'

class MenuItem(models.Model):
    item = models.CharField(max_length=75, help_text='Enter the name of the dish.')
    description = models.CharField(max_length=450, help_text='Enter a description of the dish.')
    cost = models.DecimalField(max_digits = 8, decimal_places=2, help_text='Enter the cost of the dish')

    def __str__(self):
        return f'{self.item}'

class TruckInstance(models.Model):

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=75, help_text='Enter the store name.')
    menu = models.ManyToManyField(MenuItem)
    location = models.CharField(max_length=75, help_text='Enter the current location.')
    contact = models.CharField(max_length=18, help_text='Enter a working number for the truck.', blank=True)
    album = models.ManyToManyField(ImageLink)

    class Meta:
        ordering = ['name', 'owner', 'location']

    def __str__(self):
        return f'{self.name}'

    def list_menu(self):
        return [f'{item.item}: {item.cost}' for item in self.menu.all()]

class SpecificOrderManager(models.manager):

    def __init__(self, query):
        self.query = query
        super().__init__()

    def get_queryset(self):
        return super().get_queryset().filter(truck=query)

class OrderInstance(models.Model):

    truck = models.ForeignKey(TruckInstance, on_delete=models.SET_NULL, null=True)
    inventory = models.ManyToManyField(MenuItem)
    objects = models.Manager()
    orders = SpecificOrderManager()

    def __str__(self):
        return f'{truck.name}'

    def display_inventory(self):
        return ', '.join([item.item for item in inventory])

    def list_inventory(self):
        checkout = {}
        for item in self.inventory.all():
            if item.item in checkout:
                checkout[item.item] += 1
            else:
                checkout[item.item] = 1
        ret = [f'{checkout[item.item]}*{item.item}: {item.cost*checkout[item.item]}' for item in self.inventory.all()]
        ret.append(f'total: {sum([item.cost for item in self.inventory.all()])}')
        return ret

    display_inventory.short_description = 'items'