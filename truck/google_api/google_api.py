import requests

url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyBJeC1z8iqvg7uRL4CZjdWeMaZe5o1vmDE'
# myobj = {'somekey': 'somevalue'}

x = requests.post(url)

print(x.text)
