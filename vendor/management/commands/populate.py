from django.core.management.base import BaseCommand
from faker import Faker
from random import randint
from vendor.models import *

class Command(BaseCommand):
    help = 'Populate the database'

    def handle(self, *args, **options):
        Popsicle.objects.get_or_create(flavor='Chocolate', price='250')
        Popsicle.objects.get_or_create(flavor='Coco', price='150')
        Popsicle.objects.get_or_create(flavor='Morango', price='100')
        Popsicle.objects.get_or_create(flavor='Leite Condensado', price='250')

        i = Machine.objects.get_or_create(label='joao')[0]
        j = Machine.objects.get_or_create(label='ludi')[0]

        Location.objects.get_or_create(lat='14.1234567', lng='12.1234567', machine=i)[0]
        Location.objects.get_or_create(lat='14.1234567', lng='12.1234567', machine=j)[0]

        u = User.objects.get_or_create(username='admin', is_staff=True, is_superuser=True)[0]
        u.set_password('admin')
        u.save()
        u = User.objects.get_or_create(username='teste')[0]
        u.set_password('teste')
        u.machines.set([i, j])
        u.save()


        faker = Faker()

        for pop in Popsicle.objects.all():
            PopsicleEntry.objects.get_or_create(popsicle=pop, machine=i, amount=1000)
            PopsicleEntry.objects.get_or_create(popsicle=pop, machine=j, amount=1000)

            for _ in range(1, 20):
                date = faker.past_date(start_date="-30d", tzinfo=None)
                amount = randint(1, 5)
                Purchase.objects.get_or_create(popsicle=pop, machine=i, amount=amount, date=date)
