from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from vendor.models import Popsicle, Machine, Location, Stock, Transaction
from vendor.serializers import (PopsicleSerializer, MachineSerializer,
	LocationSerializer, StockSerializer, TransactionSerializer)

class PopsicleViewSet(viewsets.ModelViewSet):
	"""Endpoints to handle Popsicle"""
	queryset = Popsicle.objects.all()
	serializer_class = PopsicleSerializer

	def destroy(self, request, *args, **kwargs):
		"""Set active attribute as false"""
		return self.change_status(False, kwargs["pk"])

	@detail_route(methods=['post'])
	def reactivate(self, request, *args, **kwargs):
		"""Set active attribute as true"""
		return self.change_status(True, kwargs["pk"])

	def change_status(self, active, popsicle_id):
		try:
			pop = Popsicle.objects.get(id=popsicle_id)
			pop.is_active = active
			pop.save()
			response = Response(status=status.HTTP_204_NO_CONTENT)
		except Popsicle.DoesNotExist:
			response = Response(status=status.HTTP_404_NOT_FOUND)
		except Exception:
			response = Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

		return response


class MachineViewSet(viewsets.ModelViewSet):
	"""Endpoints to handle Machine"""
	queryset = Machine.objects.all()
	serializer_class = MachineSerializer

	def destroy(self, request, *args, **kwargs):
		"""Set active attribute as false"""
		return self.change_status(False, kwargs["pk"])

	@detail_route(methods=['post'])
	def reactivate(self, request, *args, **kwargs):
		"""Set active attribute as true"""
		return self.change_status(True, kwargs["pk"])

	def change_status(self, active, popsicle_id):
		try:
			pop = Machine.objects.get(id=popsicle_id)
			pop.is_active = active
			pop.save()
			response = Response(status=status.HTTP_204_NO_CONTENT)
		except Machine.DoesNotExist:
			response = Response(status=status.HTTP_404_NOT_FOUND)
		except Exception:
			response = Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

		return response


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
	"""Endpoints to handle Location"""
	queryset = Location.objects.all()
	serializer_class = LocationSerializer


class StockViewSet(viewsets.ModelViewSet):
	"""Endpoints to handle Stock"""
	queryset = Stock.objects.all()
	serializer_class = StockSerializer


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
	"""Endpoints to handle Transaction"""
	queryset = Transaction.objects.all()
	serializer_class = TransactionSerializer
