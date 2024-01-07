from django.core.management.base import BaseCommand
from user.models import UserData
from django.contrib.auth.models import User
from tools.Perms import Perms

class Command(BaseCommand):
    help = 'add admin user to database'

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='+', type=str)

    def handle(self, *args, **options):
        # get userData from user
        username = options['username'][0]
        user = None
        try:
            user = User.objects.get(username=username)
        except:
            print("user not found")
            return

        userData = UserData.objects.get(user=user)

        # set permissions
        userData.permissionInteger += Perms.USER_ADMIN if userData.permissionInteger & Perms.USER_ADMIN == 0 else 0
        userData.save()
        print("user is now admin")
        