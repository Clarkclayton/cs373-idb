import json

import requests

endpoints = ['type', 'pokemon', 'move']
base_url = "http://pokeapi.co/api/v2/"

for url_endpoint in endpoints:
    resp = requests.get(base_url + url_endpoint + '/?limit=100000').json()
    for result in resp['results']:
        url = result['url']
        print(url)
        try:
            with open(url_endpoint + '_' + url.split('/')[-2] + '.json', 'w') as data_file:
                json.dump(requests.get(url).json(), data_file)
        except Exception as e:
            print(url)
