from rest_framework import serializers
from vendor.models import Popsicle, Machine, Location, Stock, Transaction


class PopsicleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Popsicle


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Location


class StockSerializer(serializers.ModelSerializer):
    popsicle = PopsicleSerializer(read_only=True)
    class Meta:
        fields = "__all__"
        model = Stock


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Transaction


class MachineSerializer(serializers.ModelSerializer):
    stock = StockSerializer(many=True, read_only=True)
    locations = LocationSerializer(many=True, read_only=True)
    class Meta:
        fields = "__all__"
        model = Machine
