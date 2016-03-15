import requests
import Models
from Models import Pokemon

endpoints = {'type': 'Types', 'pokemon': 'Pokemon', 'location': 'Location', 'move': 'Moves', 'item': 'Item'}
base_url = "http://pokeapi.co/api/v2/"


def main():
    all_data = {}
    for url_end, class_name in endpoints.items():
        resp = requests.get(base_url + url_end).json()

        urls = []
        while len(urls) != resp['count']:
            urls += [result['url'] for result in resp['results']]
            if resp['next'] is not None:
                resp = requests.get(resp['next']).json()

        x = getattr(Models, class_name)
        all_data[class_name] = [x(requests.get(url).json()) for url in urls]

if __name__ == '__main__':
    main()
