import requests
import Models

endpoints = {'type': 'Types', 'pokemon': 'Pokemon', 'location': 'Location', 'move': 'Moves', 'item': 'Item'}

base_url = "http://pokeapi.co/api/v2/"


def main():
    all_data = {}
    for url_end, class_name in endpoints.items():
        print(class_name)
        resp = requests.get(base_url + url_end).json()

        urls = []
        while len(urls) != resp['count']:
            urls += [result['url'] for result in resp['results']]
            if resp['next'] is not None:
                resp = requests.get(resp['next']).json()

        print(class_name)
        x = getattr(Models, class_name)
        all_data[class_name] = [x(requests.get(url).json()) for url in urls]
        print(class_name)

    for key, value in all_data.items():
        print (str(key) + ': ' + str(len(value)))

if __name__ == '__main__':
    main()
