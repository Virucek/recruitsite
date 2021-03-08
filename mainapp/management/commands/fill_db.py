from django.contrib.auth.models import User
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Here goes db filling...')

        # User.objects.all().delete()

        User.objects.get(username='django').delete()
        super_user = User.objects.create_superuser('django', 'django@superuser.local', 'test123')

        print('DB filled successfully')
