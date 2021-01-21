import requests
import geocoder
import googlemaps
import os
from django.http import JsonResponse

GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_API_KEY')
# print("******",GOOGLE_MAPS_API_KEY)

def google_locate():
    lat_long_url = (f'https://www.googleapis.com/geolocation/v1/geolocate?key={GOOGLE_MAPS_API_KEY}') 
    lat_long = requests.post(lat_long_url)
    print(lat_long.text)
    return lat_long

google_locate()

def test_location(request):

    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
    # Geocoding an address
    geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')[0]

    location = geocode_result['geometry']['location']
    lat = location.get("lat")
    lon = location.get("lng")
    return JsonResponse({"lat": lat, "long": lon })


# Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
# map_url = 'https://maps.googleapis.com/maps/api/staticmap?center=40.714728,-73.998672&zoom=12&size=400x400&maptype=hybrid&key=AIzaSyBJeC1z8iqvg7uRL4CZjdWeMaZe5o1vmDE'

