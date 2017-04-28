from rest_framework import serializers
from vendor.models import Popsicle, Machine, Location, Stock, Transaction


class PopsicleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Popsicle


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        extra_kwargs = {"machine": {"write_only": True}}
        exclude = ('id',)


class StockSerializer(serializers.ModelSerializer):
    popsicle = serializers.StringRelatedField()
    class Meta:
        fields = "__all__"
        model = Stock


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Transaction


class MachineSerializer(serializers.ModelSerializer):
    stocks = StockSerializer(many=True, read_only=True)
    locations = LocationSerializer(many=True, read_only=True)

    def to_representation(self, obj):
        data = super().to_representation(obj)
        machine = dict(data)
        machine["location"] = data["locations"][-1]
        machine.pop("locations")
        return machine

    class Meta:
        fields = "__all__"
        model = Machine
