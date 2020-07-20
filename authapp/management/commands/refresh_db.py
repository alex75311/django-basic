import os
import json

from django.core.management.base import BaseCommand



from authapp.models import ShopUser, UserProfile


class Command(BaseCommand):
    help = 'Refresh UserProfile in DB'

    def handle(self, *args, **options):
        users_to_update = ShopUser.objects.filter(userprofile__isnull=True)

        for user in users_to_update:
            UserProfile.objects.create(user=user)
