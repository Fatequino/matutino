import requests

from .fake_api import get_json

API_ENDPOINT = "https://run.mocky.io/v3"

# /08a52e21-95b7-4016-b233-edb4d802f34b

data = get_json()

def get_face_detail(id: int):
    # response = requests.get(_generate_url("08a52e21-95b7-4016-b233-edb4d802f34b"))
    # data = response.json()
    # data = get_json()

    return data[id - 1]['name']

def _generate_url(path: str):
    return API_ENDPOINT + '/' + path


if __name__ == '__main__':
    print(get_face_detail(2))