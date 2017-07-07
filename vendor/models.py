from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator
from datetime import date

class Popsicle(models.Model):
    flavor = models.CharField(max_length=50, unique=True, null=False, blank=False)
    price = models.CharField(max_length=4, default='100')

    def __str__(self):
        return "{}".format(self.flavor)


class Machine(models.Model):
    label = models.CharField(max_length=50, default="")
    seller = models.ForeignKey(User, related_name='machines', null=True, blank=True)
    price = models.CharField(max_length=50, default='100')

    def __str__(self):
        return "{}'s machine: #{}".format(self.label, self.id, self.locations.last())


class Temperature(models.Model):
    temp = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE,
        related_name="temperatures"
    )


class Location(models.Model):
    lat = models.CharField(max_length=15, default="")
    lng = models.CharField(max_length=15, default="")
    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE,
        related_name="locations"
    )
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "(lat:{},lng:{}) at {}".format(self.lat, self.lng, self.updated_at)


class Stock(models.Model):
    popsicle = models.ForeignKey(
        Popsicle,
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(default=0)
    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE,
        related_name="stocks"
    )
    updated_at = models.DateField(auto_now=True)


class Transaction(models.Model):
    class Meta:
        abstract = True

    popsicle = models.ForeignKey(Popsicle, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(
        default=0, validators=[MinValueValidator(1)]
    )
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)


class Purchase(Transaction):
    lid_was_released = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {} - {} @ #{}".format(self.popsicle, self.amount, self.date, self.machine.id)


class PopsicleEntry(Transaction):
    pass

class PopsicleRemoval(Transaction):
    pass

@receiver(post_save, sender=Purchase)
@receiver(post_save, sender=PopsicleRemoval)
def remove_from_stock(sender, instance, created, **kwargs):
    if created:
        stock = Stock.objects.get(
            popsicle=instance.popsicle, machine=instance.machine
        )
        stock.amount -= instance.amount
        stock.save()

@receiver(post_save, sender=PopsicleEntry)
def add_to_stock(sender, instance, created, **kwargs):
    if created:
        stock = Stock.objects.get(
            popsicle=instance.popsicle, machine=instance.machine
        )
        stock.amount += instance.amount
        stock.save()

@receiver(post_save, sender=Machine)
def create_stocks_for_machine(sender, instance, created, **kwargs):
    if created:
        stocks = []
        for pop in Popsicle.objects.all():
            stocks.append(Stock(machine=instance, popsicle=pop, amount=0))
        Stock.objects.bulk_create(stocks)

@receiver(post_save, sender=Popsicle)
def create_stocks_for_popsicle(sender, instance, created, **kwargs):
    if created:
        stocks = []
        for machine in Machine.objects.all():
            stocks.append(Stock(machine=machine, popsicle=instance, amount=0))
        Stock.objects.bulk_create(stocks)

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
