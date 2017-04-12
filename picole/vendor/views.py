from rest_framework import viewsets, status
from rest_framework.response import Response
from vendor.models import Popsicle, Machine, Location, Stock, Transaction
from vendor.serializers import PopsicleSerializer
#, MachineSerializer, LocationSerializer, StockSerializer, TransactionSerializer

class PopsicleViewSet(viewsets.ModelViewSet):
	"""Endpoints to handle Popsicle"""
	queryset = Popsicle.objects.all()
	serializer_class = PopsicleSerializer

	def destroy(self, request, *args, **kwargs):
		try:
			pop = Popsicle.objects.get(id=kwargs["pk"])
			pop.is_active = False
			pop.save()
			response = Response(status_code=status.HTTP_204_NO_CONTENT)
		except Popsicle.DoesNotExist:
			response = Response(status_code=status.HTTP_404_NOT_FOUND)
		except Exception:
			response = Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

		return response
