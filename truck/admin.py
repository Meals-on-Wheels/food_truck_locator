from django.contrib import admin
from .models import TruckInstance, Image, MenuItem

# Register your models here.
@admin.register(TruckInstance)
class TruckInstanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'description', 'cost')

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title',)