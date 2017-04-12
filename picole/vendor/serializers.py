from rest_framework import serializers
from vendor.models import Popsicle, Machine, Location, Stock, Transaction


class PopsicleSerializer(serializers.ModelSerializer):
	class Meta:
		fields = "__all__"
		model = Popsicle
