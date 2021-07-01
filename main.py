import requests
import json
import datetime

APP_ID = 7890822
BASE_URL = 'https://oauth.vk.com/authorize'
auth_data = {
    'client_id': APP_ID,
    'display': 'page',
    'response_type': 'token',
    'scope': 'status',
    'v': '5.126',
    'redirect_uri': 'https://example.com/'
}

TOKEN = '111'
YA_TOKEN = '111'


class VkUser:
    def __init__(self, token, user_id=None, first_name=None, last_name=None):
        self.token = token
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name

    def get_params(self):
        return dict(
            access_token=self.token,
            v='5.126'
        )

    def mkdir_ya(self):
        ya_headers = {
            'Accept': 'application/json',
            'Authorization': YA_TOKEN
        }
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        dirname = '/' + str(main_user_id)
        ya_params = {'path': dirname}
        response = requests.put(upload_url, params=ya_params, headers=ya_headers)
        if response.status_code == 201:
            print('Папка на Я.Диск создана')
        return

    def get_photos(self):
        """
        дёргаем фоточки пользователя
        """
        params = self.get_params()
        params['owner_id'] = main_user_id
        params['album_id'] = 'profile'
        params['extended'] = 1
        params['count'] = number_of_photos
        response = requests.get(
            'https://api.vk.com/method/photos.get',
            params
        )

        vk_response = response.json()
        count_userpics = vk_response['response']['count']  # кол-во юзерпиков у юзера (не более number_of_photos)
        print(f'всего юзерпиков ', count_userpics)
        likes_list = []
        for x in range(count_userpics):
            # кол-во лайков юзерпика
            likes_count = vk_response['response']['items'][x]['likes']['count']
            likes_list.append(likes_count)
            print(likes_list)
            print(f'Юзерпик, у которого ', likes_count, 'лайков')

            # дата загрузки фото
            photo_datetime = vk_response['response']['items'][x]['date']
            data_value = datetime.datetime.fromtimestamp(photo_datetime)
            data_string = data_value.strftime('%Y-%m-%d')

            # тип и урл самого большого [-1] - последний в списке - юзерпика
            pic_type = vk_response['response']['items'][x]['sizes'][-1]['type']
            pic_url = vk_response['response']['items'][x]['sizes'][-1]['url']

            # заливаем на Я.Диск
            ya_headers = {
                'Accept': 'application/json',
                'Authorization': YA_TOKEN
            }
            upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
            if likes_list.count(likes_count) == 1:
                filename = '/' + str(main_user_id) + '/' + str(likes_count)
                print(filename)
            else:
                filename = '/' + str(main_user_id) + '/' + str(likes_count) + '_' + str(data_string)
                print(filename)
            ya_params = {'path': filename, 'url': pic_url}
            response = requests.post(upload_url, params=ya_params, headers=ya_headers)
            if response.status_code == 202:
                print('Файл загружен на Я.Диск')
            # залили на Я.Диск

            # собираем json с параметрами фото
            photo_data = {
                'counter': x,
                'items': {
                    'file_name': filename,
                    'size': pic_type
                }
            }
            with open('photo_data.json', 'a') as write_file:
                json.dump(photo_data, write_file)

        return


username = VkUser(TOKEN)
# main_user_id = 171691064
main_user_id = 62117789  # это я
# main_user_id = 23212039  # это Степа
number_of_photos = 5  # максимальное количество загружаемых фотографий

username.mkdir_ya()
username.get_photos()

