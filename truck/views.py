from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views import generic
from .models import TruckInstance, ImageLink, MenuItem

# Create your views here.
# request.query.lat ???
def test_map_view(request):
    info = {
        'lat': 40.714224,
        'lng': -73.961452
    }
    return render(
        request, "map2.html", context = info
    )
