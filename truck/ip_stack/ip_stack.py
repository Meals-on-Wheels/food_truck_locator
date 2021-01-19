# Works but location is to far away from actual

import requests
import json

def ip_static_locator():
    send_url = "http://api.ipstack.com/check?access_key=86a56dc7c1b3d9a9ac5742ae357fb74f"
    geo_req = requests.get(send_url)
    geo_json = json.loads(geo_req.text)
    latitude = geo_json['latitude']
    longitude = geo_json['longitude']
    city = geo_json['city']
    print(city, latitude, longitude)

ip_static_locator()
