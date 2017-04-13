from rest_framework import viewsets, status, mixins
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


class LocationViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin):
	"""Endpoints to handle Location"""
	queryset = Location.objects.all()
	serializer_class = LocationSerializer

	def create(self, request):
		"""Create new location for machines.

		If machine's location has the same latitude and longitude, given the
		precision, it won't be updated.

		Required Params:
		- **latitude**: {String} Vertical location with four decimal places precision
		- **longitude**: {String} Horizontal location with four decimal places precision
		- **machine**: {PK (int)} ID from machine"""

		longitude = request.data["longitude"][:-3]
		latitude = request.data["latitude"][:-3]

		try:
			machine = Machine.objects.get(id=request.data["machine"])
			loc = machine.locations.last()
			if not (loc.latitude.startswith(latitude) and loc.longitude.startswith(longitude)):
				response = super().create(request)
			else:
				response = Response(status=status.HTTP_200_OK)
		except Machine.DoesNotExist:
			response = Response("Invalid Machine", status=status.HTTP_400_BAD_REQUEST)

		return response


class StockViewSet(viewsets.ModelViewSet):
	"""Endpoints to handle Stock"""
	queryset = Stock.objects.all()
	serializer_class = StockSerializer


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
	"""Endpoints to handle Transaction"""
	queryset = Transaction.objects.all()
	serializer_class = TransactionSerializer
