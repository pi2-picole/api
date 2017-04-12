from django.db import models

# Create your models here.
class Popsicle(models.Model):
	flavor = models.CharField(max_length=25, default="")
	is_active = models.BooleanField(default=True)


class Machine(models.Model):
	is_active = models.BooleanField(default=True)
	label = models.CharField(max_length=25, default="")	


class Location(models.Model):
	latitude = models.CharField(max_length=15, default="")
	longitude = models.CharField(max_length=15, default="")
	machine = models.ForeignKey(
		Machine,
		on_delete=models.DO_NOTHING,
		limit_choices_to={'is_active': True}
	)
	updated_at = models.DateTimeField(auto_now_add=True)


class Stock(models.Model):
	popsicle = models.ForeignKey(
		Popsicle,
		on_delete=models.DO_NOTHING,
		limit_choices_to={'is_active': True}
	)
	price = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
	amount = models.PositiveSmallIntegerField(default=0)
	machine = models.ForeignKey(
		Machine,
		on_delete=models.DO_NOTHING,
		limit_choices_to={'is_active': True}
	)
	updated_at = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
	popsicle = models.ForeignKey(
		Popsicle,
		on_delete=models.DO_NOTHING,
		limit_choices_to={'is_active': True}
	)
	quantity = models.PositiveSmallIntegerField(default=0)
	machine = models.ForeignKey(
		Machine,
		on_delete=models.DO_NOTHING,
		limit_choices_to={'is_active': True}
	)
	timestamp = models.DateTimeField(auto_now_add=True)
	lid_was_released = models.BooleanField(default=False)
	is_withdraw = models.BooleanField(default=False)
	is_purchase = models.BooleanField(default=False)
