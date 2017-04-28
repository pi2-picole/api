from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from vendor.models import Popsicle, Machine, Location, Stock, Transaction
from vendor.serializers import (PopsicleSerializer, MachineSerializer,
    LocationSerializer, StockSerializer, TransactionSerializer)

class PopsicleViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin,
                    mixins.UpdateModelMixin):
    """Endpoints to handle Popsicle"""
    queryset = Popsicle.objects.all()
    serializer_class = PopsicleSerializer

    @detail_route(methods=['post'])
    def deactivate(self, request, *args, **kwargs):
        """Set active attribute as true"""
        return self.change_status(False, kwargs["pk"])

    @detail_route(methods=['post'])
    def activate(self, request, *args, **kwargs):
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


class MachineViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin,
                    mixins.UpdateModelMixin):
    """Endpoints to handle Machine"""
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

    @detail_route(methods=['post'])
    def deactivate(self, request, *args, **kwargs):
        """Set active attribute as true"""
        return self.change_status(False, kwargs["pk"])

    @detail_route(methods=['post'])
    def activate(self, request, *args, **kwargs):
        """Set active attribute as true"""
        return self.change_status(True, kwargs["pk"])

    def change_status(self, active, mach_id):
        try:
            machine = Machine.objects.get(id=mach_id)
            machine.is_active = active
            machine.save()
            response = Response(status=status.HTTP_204_NO_CONTENT)
        except Machine.DoesNotExist:
            response = Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            response = Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return response


class LocationViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """Endpoints to handle Location"""
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    MIN_SIZE = 10

    def create(self, request):
        """Create new location for machines.

        If machine's location has the same latitude and longitude, given the
        precision, it won't be updated.

        Required Params:
        - **latitude**: {String} Vertical location with seven decimal places precision
        - **longitude**: {String} Horizontal location with seven decimal places precision
        - **machine**: {PK (int)} ID from machine"""

        if len(request.data['longitude']) < self.MIN_SIZE or \
                len(request.data['latitude']) < self.MIN_SIZE:
            message = 'Longitude and Latitude must be at least {} characters long'.format(self.MIN_SIZE)
            return Response(message,status=status.HTTP_400_BAD_REQUEST)

        longitude = request.data["longitude"][:-2]
        latitude = request.data["latitude"][:-2]

        try:
            machine = Machine.objects.get(id=request.data["machine"])
            loc = machine.locations.last()
            if (not loc) or not (loc.latitude.startswith(latitude) and loc.longitude.startswith(longitude)):
                response = super().create(request)
            else:
                response = Response(status=status.HTTP_204_NO_CONTENT)
        except Machine.DoesNotExist:
            response = Response("Invalid Machine", status=status.HTTP_400_BAD_REQUEST)

        return response


class StockViewSet(viewsets.ModelViewSet):
    """Endpoints to handle Stock"""
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class TransactionViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin):
    """Endpoints to handle Transaction"""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
