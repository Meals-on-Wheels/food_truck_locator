import requests
import geocoder
import googlemaps
from datetime import datetime

lat_long_url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyBJeC1z8iqvg7uRL4CZjdWeMaZe5o1vmDE'
map_url = 'https://maps.googleapis.com/maps/api/staticmap?center=40.714728,-73.998672&zoom=12&size=400x400&maptype=hybrid&key=AIzaSyBJeC1z8iqvg7uRL4CZjdWeMaZe5o1vmDE'

# Most accurate locator (GOOGLE)
def google_locate():
    lat_long = requests.post(lat_long_url)
    print(lat_long.text)
    return lat_long






# 2nd most accurate
g = geocoder.ip('me')
# print(g.latlng)


# Google Maps 
gmaps = googlemaps.Client(key='AIzaSyBJeC1z8iqvg7uRL4CZjdWeMaZe5o1vmDE')
# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("Sydney Town Hall",
                                     "Parramatta, NSW",
                                     mode="transit",
                                     departure_time=now)

# print('Geocode:',geocode_result)
# print('Reverse Geo Code:',reverse_geocode_result)
# print('Directions Result:',directions_result)


