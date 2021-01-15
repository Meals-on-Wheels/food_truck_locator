import requests, os

url = "https://us1.locationiq.com/v1/search.php"

data = {
    'key': 'pk.485c2f6d43a43b7d0283ca56b079855c',
    'q': 'Empire State Building',
    'format': 'json'
}

response = requests.get(url, params=data)

print(response.text)
