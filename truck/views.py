from django.shortcuts import render
from django.views import View

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
