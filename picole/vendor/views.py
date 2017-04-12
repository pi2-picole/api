from rest_framework import viewsets
from vendor.models import Popsicle, Machine, Location, Stock, Transaction
from vendor.serializers import PopsicleSerializer
#, MachineSerializer, LocationSerializer, StockSerializer, TransactionSerializer

class PopsicleViewSet(viewsets.ModelViewSet):
	queryset = Popsicle.objects.all()
	serializer_class = PopsicleSerializer
