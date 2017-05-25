from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAdminUser
from vendor import models, serializers

import requests
import json

class GenericModelViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin,
                    mixins.UpdateModelMixin):

    @detail_route(methods=['delete'])
    def deactivate(self, request, *args, **kwargs):
        """Set active attribute as true"""
        return self.change_status(False, kwargs["pk"])

    @detail_route(methods=['post'])
    def activate(self, request, *args, **kwargs):
        """Set active attribute as true"""
        return self.change_status(True, kwargs["pk"])

    def change_status(self, active, pk):
        model = self.get_class()
        try:
            obj = model.objects.get(id=pk)
            obj.is_active = active
            obj.save()
            response = Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            response = Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            response = Response(
                "Something wrong happened, check with the system admin.",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return response

    def get_class(self):
        raise NotImplementedError('Subclass must implement this')

class PopsicleViewSet(GenericModelViewSet):
    """Endpoints to handle Popsicle"""
    queryset = models.Popsicle.objects.all()
    serializer_class = serializers.PopsicleSerializer

    def get_class(self):
        return models.Popsicle


class MachineViewSet(GenericModelViewSet):
    """Endpoints to handle Machine"""
    queryset = models.Machine.objects.all()
    serializer_class = serializers.MachineSerializer

    def get_class(self):
        return models.Machine


class LocationViewSet(viewsets.GenericViewSet):
    """Endpoints to handle Location"""
    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer
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


class PopsicleRemovalViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = models.PopsicleRemoval.objects.all()
    serializer_class = serializers.PopsicleRemovalSerializer


class PopsicleEntryViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = models.PopsicleEntry.objects.all()
    serializer_class = serializers.PopsicleEntrySerializer


class PurchaseViewSet(viewsets.GenericViewSet):
    queryset = models.Purchase.objects.all()
    serializer_class = serializers.PurchaseSerializer

    def create(self, request):
        """Create a new purchase.

        **machine_id**: Int

        **popsicles** Array of dictionaries (objects). Each dict has to have these keys:
        flavor, amount, price, popsicle_id.

        Ex:
        ```
        {
            "machine_id": 1,
            "popsicles": [
                { "amount":1, "flavor": "Chocolate", "price": "150", "popsicle_id": 1 },
                { "amount":2, "flavor": "Coco", "price": "100", "popsicle_id": 2 }
            ]
        }
        ```
        """
        items = []
        purchases = []
        for pop in request.data["popsicles"]:
            item = {
                "Name": pop["flavor"],
                "Description": "Picole",
                "UnitPrice": pop["price"],
                "Quantity": pop["amount"],
                "Type": "Asset",
            }
            items.append(item)

            purchase = Purchase(
                popsicle_id=pop["popsicle_id"],
                amount=pop["amount"],
                machine=request.data["machine_id"]
            )

        models.Purchase.objects.bulk_create(purchases)

        data = {
            "SoftDescriptor": "Picole",
            "Cart": {
                "Items": items
            },
            "Shipping": {
                "Type": "WithoutShippingPickUp",
            },
        }

        headers = {"Content-Type": "application/json", "MerchantId": "43c539f0-1366-41e6-a59e-1b611e7d43c0"}
        url = "https://cieloecommerce.cielo.com.br/api/public/v1/orders"
        r = requests.post(url, json=data, headers=headers)

        text = json.loads(r.text)

        return Response(text['settings'], status=r.status_code)


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAdminUser, )
