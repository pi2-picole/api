from django.db.utils import IntegrityError
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


class TransactionViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin):
    """Endpoints to handle Transaction"""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request):
        data = request.data
        try:
            stock = Stock.objects.get(popsicle_id=int(data["popsicle"]), machine_id=int(data["machine"]))
            response = self.update_stock(data, stock, request)
        except Stock.DoesNotExist:
            response = self.create_stock(data, request)
        return response

    def update_stock(self, data, stock, request):
        response = None

        if data["is_purchase"] or data["is_withdraw"]:
            if stock.amount - int(data["quantity"]) >= 0:
                stock.amount -= int(data["quantity"])
            else:
                msg = "Not enough popsicles. There is only {} left.".format(stock.amount)
                response = Response(msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            if int(data["quantity"]) > 0:
                stock.amount += int(data["quantity"])
            else:
                response = Response("Cannot subtract popsicles while adding to the stock", status=status.HTTP_400_BAD_REQUEST)


        if response is None:
            stock.save()
            response = super().create(request)

        return response

    def create_stock(self, data, request):
        if not data["is_withdraw"]:
            data["is_purchase"] = False
            stock_data = {
                "popsicle_id": data["popsicle"],
                "machine_id": data["machine"],
                "amount": data["quantity"],
            }
            try:
                stock = Stock.objects.create(**stock_data)
                response = super().create(request)
            except IntegrityError:
                response = Response("Popsicle does not exist.", status=status.HTTP_400_BAD_REQUEST)
        else:
            response = Response("Can't withdraw from empty stock", status=status.HTTP_400_BAD_REQUEST)

        return response
