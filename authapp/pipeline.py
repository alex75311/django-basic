from social_core.exceptions import AuthForbidden
import requests

from authapp.models import ShopUser
from djangobasic.settings import MEDIA_ROOT


def save_user_profile(backend, user, response, *args, **kwargs):
    print(response)
    if backend.name == 'google-oauth2':
        if 'picture' in response.keys():
            picture = requests.get(response['picture']).content
            file_name = f'users_avatars/{user.username}_logo.jpg'
            with open(f'{MEDIA_ROOT}/{file_name}', 'wb') as f:
                f.write(picture)
            user.avatar = file_name
        if 'locale' in response.keys():
            user.userprofile.locale = response['locale']

    elif backend.name == 'vk-oauth2':
        if 'photo' in response.keys():
            picture = requests.get(response['photo']).content
            file_name = f'users_avatars/{user.username}_logo.jpg'
            with open(f'{MEDIA_ROOT}/{file_name}', 'wb') as f:
                f.write(picture)
            user.avatar = file_name

    user.save()
