import requests
import json
from progress.bar import IncrementalBar
from datetime import datetime

with open('token.txt', 'r') as file_object:
    token = file_object.read().strip()

with open('token_ya.txt', 'r') as file_object:
    token_ya = file_object.read().strip()


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def photos_get(self):
        # ### получение полного списка фото пользователя
        owner_id = int(input('Введите ID пользователя: '))
        photos_get_url = self.url + 'photos.get'
        photos_get_params = {
            'owner_id': owner_id,
            'album_id': 'profile',
            'extended': 1
        }
        req = requests.get(photos_get_url, params={**self.params, **photos_get_params}).json()['response']['items']
        likes_url_dict = {}
        json_list = []
        like_list = []

        for photo in req:
            likes = photo['likes']['count']
            date = datetime.utcfromtimestamp(photo['date']).strftime('%Y-%m-%d-%HH-%MM-%SS')
            size = photo['sizes'][-1]['type']
            photo_url = photo['sizes'][-1]['url']
            if f'{likes}.jpg' not in like_list:
                likes_url_dict[f'{likes}.jpg'] = photo_url
                json_list.append({'file_name': f'{likes}.jpg', 'size': size})
                like_list.append(f'{likes}.jpg')
            else:
                likes_url_dict[f'{likes} {date}.jpg'] = photo_url
                json_list.append({'file_name': f'{likes} {date}.jpg', 'size': size})

        with open('photo_data.json', 'w') as outfile:
            json.dump(json_list, outfile, indent=4)
        return likes_url_dict


class YandexDisk:
    def __init__(self, token_ya: str):
        self.token = token_ya

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def _create_directory(self):
        directory_name = input('Введите имя папки для создания: ')
        headers = self.get_headers()
        params = {'path': directory_name}
        dir_query = 'https://cloud-api.yandex.net/v1/disk/resources/'
        requests.put(dir_query, headers=headers, params=params)
        return directory_name

    def upload_photo(self, photo_dict):
        upload_query = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        directory = self._create_directory()
        status_bar = IncrementalBar('Upload process', max=len(photo_dict))
        for name, url in photo_dict.items():
            params = {
                'path': f'{directory}/{name}',
                'url': url
            }
            requests.post(upload_query, params=params, headers=headers)
            status_bar.next()
        status_bar.finish()
        return print('Upload success')


if __name__ == '__main__':
    VkUser = VkUser(token, '5.131')
    photos = VkUser.photos_get()
    YandexDisk = YandexDisk(token_ya)
    upload_to_YandexDisk = YandexDisk.upload_photo(photos)
