import requests
import geocoder
import googlemaps
import os
from django.http import JsonResponse

# var = truckinstance.objects.all()

# env = environ.Env(
#     DEBUG =(bool, False)
# )

# environ.Env.read_env()

GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_API_KEY')
print("******",GOOGLE_MAPS_API_KEY)

def google_locate():
    lat_long = requests.post(lat_long_url)
    print(lat_long.text)
    return lat_long


def test_location(request):
"""
Post users address to this rout
address gets converted to lat long
retrieve location of trucks from databases
****template stuff from here*****
pinning trucks on to map
users lat lon
"""

    lat_long_url = (f'https://www.googleapis.com/geolocation/v1/geolocate?key={GOOGLE_MAPS_API_KEY}')
    map_url = 'https://maps.googleapis.com/maps/api/staticmap?center=40.714728,-73.998672&zoom=12&size=400x400&maptype=hybrid&key=AIzaSyBJeC1z8iqvg7uRL4CZjdWeMaZe5o1vmDE'
    # Most accurate locator (GOOGLE)
    # Google Maps 
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
    # Geocoding an address
    geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')[0]
    # Look up an address with reverse geocoding
    reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

    location = geocode_result['geometry']['location']
    lat = location.get("lat")
    lon = location.get("lng")
    return JsonResponse({"lat": lat, "long": lon })



#print('Geocode:',geocode_result)
# print('Reverse Geo Code:',reverse_geocode_result)
# print('Directions Result:',directions_result)

#unfold(geocode_result)
# print(lat)
# print(lon)
