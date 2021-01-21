import os
import environ
import requests
import googlemaps

def google_locate():
    lat_long_url = (f'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyBJeC1z8iqvg7uRL4CZjdWeMaZe5o1vmDE') 
    lat_long = requests.post(lat_long_url)
    print(lat_long.text)
    return lat_long

google_locate()
