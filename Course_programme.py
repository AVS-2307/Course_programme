import time
import requests

from pprint import pprint
import json

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

    def all_photos_get(self):
        # ### получение полного списка фото пользователя
        owner_id = int(input('Введите ID пользователя: '))
        photos_get_url = self.url + 'photos.get'
        photos_get_params = {
            'owner_id': owner_id,
            'album_id': 'profile',
            'extended': 1
        }

        req = requests.get(photos_get_url, params={**self.params, **photos_get_params}).json()
        return req['response']['items']

    def photos_required_get(self, all_photos_get):
        # ### получение размера фото 'type' и ссылки 'url' на фото пользователя
        photo_list = all_photos_get[0]['sizes']
        photo_list_sorted = sorted(photo_list, key=lambda x: x['type'], reverse=True)
        # photo_dict_ = {}
        # for photo in photo_list_sorted:
        #     photo_dict_ = photo_dict.update({photo['type'], photo['url']})
        for photo in photo_list_sorted:
            photo_dict = {'name': photo['type'], 'url': photo['url']}

        # with open(req, 'w') as outfile:
        #     a = json.dump(req, outfile)
        #     print(json.dumps(a, indent=2))


class YandexDisk:
    def __init__(self, token_ya: str):
        self.token = token_ya

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAth {self.token}'
        }

    def _get_upload_link(self, disk_file_path):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': disk_file_path, 'overwrite': 'false'}
        response = requests.get(upload_url, headers=headers, params=params)
        pprint(response.json())
        return response.json()

    def upload_photo(self, photo_dict: dict):
        headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}
        for name, url in photo_dict.items():
            params = {
                'path': f'Vk_Photos/{name}.jpg',
                'url': f'{url}'
            }
            requests.post(url='https://cloud-api.yandex.net/v1/disk/resources/upload', params=params, headers=headers)


# from progress.bar import IncrementalBar

# bar = IncrementalBar('Countdown', max = len(photo_dict))
#
# for item in mylist:
#     bar.next()
#     time.sleep(1)
#
# bar.finish()

if __name__ == '__main__':
    VkUser = VkUser(token, '5.131')
    all_photos = VkUser.all_photos_get()
    VkUser.photos_required_get(all_photos)
    ya = YandexDisk(token_ya)

    ya.upload_photo('Vk_Photos/', )
