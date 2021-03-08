from django.contrib.auth.models import User
from django.core.management import BaseCommand

from authapp.models import IndustryType


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Here goes db filling...')

        # User.objects.all().delete()
        # IndustryType.objects.all().delete()
        #
        # types_ = [
        #     'IT',
        #     'Банковские услуги',
        #     'Маркетинг',
        #     'Бухгалтерия'
        # ]
        # for type_ in types_:
        #     IndustryType.objects.create(descx=type_)

        User.objects.get(username='django').delete()
        User.objects.create_superuser('django', 'django@superuser.local', 'test123')

        print('DB filled successfully')
