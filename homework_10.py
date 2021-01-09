import requests


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, vk_token, version):
        """Конструктор класса VkUser."""
        self.token = vk_token
        self.version = version
        self.params = {
            'access_token': self.token,
            'v': self.version
        }
        self.owner_id = requests.get(self.url + 'users.get', self.params).json()['response'][0]['id']

    def __str__(self):
        """Выведет на экран ссылку на профиль пользователя VK"""
        return 'https://vk.com/id' + str(self.owner_id)

    def __and__(self, some_user):
        """Выведет на экран список общих друзей двух экземпляров класса VkUser"""
        if not isinstance(some_user, VkUser):
            return f'Ошибка: обьект {some_user} не принадлежит классу VkUser'
        else:
            common_friends = self.get_mutual_friends(some_user.owner_id)
            return common_friends

    def get_friends(self, user_id=None):
        """Возвратит список ids друзей пользователей VK."""
        if user_id is None:
            user_id = self.owner_id
        friends_url = self.url + 'friends.get'
        friends_params = {
            'user_id': user_id
        }
        res = requests.get(friends_url, params={**self.params, **friends_params}).json()
        return res['response']['items'] if 'error' not in res.keys() else res['error']['error_msg']

    def get_mutual_friends(self, target_uid, source_uid=None):
        """Возвратит список обьектов общих друзей пользователей VK."""
        mutual_friends_url = self.url + 'friends.getMutual'
        if source_uid is None:
            source_uid = self.owner_id
        friends_params = {
            'source_uid': source_uid,
            'target_uid': target_uid
        }
        res = requests.get(mutual_friends_url, params={**self.params, **friends_params}).json()['response']
        return self.get_user_info(','.join(map(str, res)))

    def get_user_info(self, user_ids=None):
        """Примет перечисленные через запятую ids пользователей,
        возвратит список обьектов пользователей VK."""
        users_info_url = self.url + 'users.get'
        if user_ids is None:
            user_ids = self.owner_id
        users_info_params = {
            'user_ids': user_ids
        }
        res = requests.get(users_info_url, params={**self.params, **users_info_params}).json()['response']
        return res


# with open('my_token.txt', 'r') as file_object:
#     my_token = file_object.read().strip()
#
# with open('token.txt', 'r') as file_object:
#     token = file_object.read().strip()
#
# vk_client_1 = VkUser(my_token, '5.126')
# vk_client_2 = VkUser(token, '5.126')

# print(vk_client_1.owner_id)
# print(vk_client_2.owner_id)

# print(vk_client_1.get_friends())
# print(vk_client_2.get_friends())

# print(vk_client_1 & vk_client_2)
# print(vk_client_1.get_mutual_friends(2294694))
# print(vk_client_1.get_user_info(2294694))
