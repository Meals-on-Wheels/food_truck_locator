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

    owner = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=75, help_text='Enter the store name.')
    menu = models.ManyToManyField(MenuItem)
    location = models.CharField(max_length=75, help_text='Enter the current location.')
    contact = models.CharField(max_length=18, help_text='Enter a working number for the truck.', blank=True)
    album = models.ManyToManyField(ImageLink)

    class Meta:
        ordering = ['name', 'owner', 'location']

    def __str__(self):
        return f'{self.name}'