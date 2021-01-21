from django.contrib import admin
from .models import TruckInstance, ImageLink, MenuItem, OrderInstance, UserLocation

# Register your models here.
@admin.register(UserLocation)
class UserLocationAdmin(admin.ModelAdmin):
    list_display = ('user', 'lat', 'lng', 'latlng')

@admin.register(TruckInstance)
class TruckInstanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'description', 'cost')

@admin.register(ImageLink)
class ImageLinkAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(OrderInstance)
class OrderInstanceAdmin(admin.ModelAdmin):
    list_display = ('order', 'display_inventory',)
