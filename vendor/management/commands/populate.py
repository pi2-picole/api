from django.core.management.base import BaseCommand
from vendor.models import *

class Command(BaseCommand):
    help = 'Populate the database'

    def handle(self, *args, **options):
        a = Popsicle.objects.get_or_create(flavor='Chocolate', price='250')[0]
        b = Popsicle.objects.get_or_create(flavor='Coco', price='150')[0]
        c = Popsicle.objects.get_or_create(flavor='Morango', price='100')[0]
        d = Popsicle.objects.get_or_create(flavor='Leite Condensado', price='250')[0]

        i = Machine.objects.get_or_create(label='joao')[0]
        j = Machine.objects.get_or_create(label='ludi')[0]

        Location.objects.get_or_create(lat='14.1234567', lng='12.1234567', machine=i)[0]
        Location.objects.get_or_create(lat='14.1234567', lng='12.1234567', machine=j)[0]

        PopsicleEntry.objects.get_or_create(popsicle=a, machine=i, amount=100)[0]
        PopsicleEntry.objects.get_or_create(popsicle=b, machine=i, amount=100)[0]
        PopsicleEntry.objects.get_or_create(popsicle=c, machine=i, amount=100)[0]
        PopsicleEntry.objects.get_or_create(popsicle=d, machine=i, amount=100)[0]

        PopsicleEntry.objects.get_or_create(popsicle=a, machine=j, amount=100)[0]
        PopsicleEntry.objects.get_or_create(popsicle=b, machine=j, amount=100)[0]
        PopsicleEntry.objects.get_or_create(popsicle=c, machine=j, amount=100)[0]
        PopsicleEntry.objects.get_or_create(popsicle=d, machine=j, amount=100)[0]

        u = User.objects.get_or_create(username='admin', is_staff=True, is_superuser=True)[0]
        u.set_password('admin')
        u.save()
        u = User.objects.get_or_create(username='teste')[0]
        u.set_password('teste')
        u.machines.set([i, j])
        u.save()
