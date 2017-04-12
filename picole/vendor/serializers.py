from rest_framework import serializers
from vendor.models import Popsicle, Machine, Location, Stock, Transaction


class PopsicleSerializer(serializers.ModelSerializer):
	class Meta:
		fields = "__all__"
		model = Popsicle


class MachineSerializer(serializers.ModelSerializer):
	class Meta:
		fields = "__all__"
		model = Machine


class LocationSerializer(serializers.ModelSerializer):
	class Meta:
		fields = "__all__"
		model = Location


class StockSerializer(serializers.ModelSerializer):
	class Meta:
		fields = "__all__"
		model = Stock


class TransactionSerializer(serializers.ModelSerializer):
	class Meta:
		fields = "__all__"
		model = Transaction
