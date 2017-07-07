from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAdminUser, AllowAny
from vendor import models, serializers
from django.contrib.auth import authenticate
from django.db.models import Sum

import requests
import json


class PopsicleViewSet(viewsets.ModelViewSet):
    """Endpoints to handle Popsicle"""
    queryset = models.Popsicle.objects.all()
    serializer_class = serializers.PopsicleSerializer


class MachineViewSet(viewsets.ModelViewSet):
    """Endpoints to handle Machine"""
    queryset = models.Machine.objects.all()
    serializer_class = serializers.MachineSerializer

    @detail_route()
    def graph_total(self, request, pk, *args, **kwargs):
        machine = self.queryset.get(pk=pk)
        data = machine.purchase_set.values('popsicle__flavor').annotate(total=Sum('amount'))
        data = list(data)
        for flavor in data:
            flavor['flavor'] = flavor.pop('popsicle__flavor')

        return Response(data)

    @detail_route()
    def graph_by_day(self, request, pk, *args, **kwargs):
        machine = self.queryset.get(pk=pk)
        data = machine.purchase_set.values('date', 'popsicle__flavor').annotate(total=Sum('amount'))
        data = list(data)
        for flavor in data:
            flavor['date'] = flavor['date'].strftime("%d/%m/%y")
            flavor['flavor'] = flavor.pop('popsicle__flavor')

        return Response(data)

    @list_route(methods=['post'])
    def alarm(self, request):
        url = 'http://picole.pagekite.me/alarm/'
        return Response(requests.post(url))


class SetupViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """Endpoints to handle Location"""
    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer
    MIN_SIZE = 10
    permission_classes = ()

    def create(self, request):
        """Create new location for machines.

        If machine's location has the same lat and lng, given the
        precision, it won't be updated.

        Required Params:
        - **lat**: String. Vertical location with seven decimal places precision
        - **lng**: String. Horizontal location with seven decimal places precision
        - **temperature**: Float. The temperature of the machine
        - **ip**: String. Format: XXX.XXX.XXX.XXX. The ip address of the machine
        - **machine**: PK (int). machine's id"""

        lng = request.data["lng"]
        lat = request.data["lat"]

        if len(lat) < self.MIN_SIZE or len(lng) < self.MIN_SIZE:
            message = 'Longitude and Latitude must be at least {} characters long'.format(self.MIN_SIZE)
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        try:
            machine = models.Machine.objects.get(id=request.data["machine"])
        except models.Machine.DoesNotExist:
            return Response("Invalid Machine", status=status.HTTP_400_BAD_REQUEST)

        if 'ip' in request.data.keys():
            machine.ip = request.data['ip']
            machine.save()

        lng = lng[:-2]
        lat = lat[:-2]
        loc = machine.locations.last()

        if (loc is None) or not (loc.lat.startswith(lat) and loc.lng.startswith(lng)):
            response = super().create(request)
        else:
            response = Response('Location has not changed since last time',
                                status=status.HTTP_204_NO_CONTENT)

        return response


class PopsicleRemovalViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = models.PopsicleRemoval.objects.all()
    serializer_class = serializers.PopsicleRemovalSerializer
    permission_classes = ()


class PopsicleEntryViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = models.PopsicleEntry.objects.all()
    serializer_class = serializers.PopsicleEntrySerializer
    permission_classes = ()


class PurchaseViewSet(viewsets.GenericViewSet):
    queryset = models.Purchase.objects.all()
    serializer_class = serializers.PurchaseSerializer
    permission_classes = ()

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

            purchase = models.Purchase.objects.create(
                popsicle_id=pop["popsicle_id"],
                amount=pop["amount"],
                machine_id=request.data["machine_id"]
            )

            purchases.append(purchase.id)

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
        ret_data = {
            'url': text['settings']['checkoutUrl'],
            'purchases': purchases
        }

        return Response(ret_data, status=r.status_code)

    @list_route(methods=['post'])
    def release(self, request):
        """Release the popsicle for the user.


        Pass an array with the ids of the purchases:
        ```
        {
            "purchases": [2, 3]
        }
        ```
        """
        purchases = models.Purchase.objects.filter(id__in=request.data['purchases'])
        popsicles = {}
        for p in purchases:
            url = 'http://picole.pagekite.me/'.format(p.machine.ip)
            popsicles[p.popsicle.id] = {
                'release': p.amount,
                'new_amount': p.machine.stocks.get(popsicle_id=p.popsicle.id).amount
            }
            p.lid_was_released = True
            p.save()

        requests.post(url, json=popsicles)

        return Response(popsicles)

    @list_route(methods=['post'])
    def test(self, request):
        return Response()


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    class UserPermission(IsAdminUser):
        def has_permission(self, request, view):
            pk = 0
            if 'pk' in view.kwargs.keys():
                pk = view.kwargs['pk']

            if view.action == 'login':
                return True
            elif view.action == 'retrieve' and not request.user.is_anonymous() and int(pk) == request.user.id:
                return True
            else:
                return super().has_permission(request, view)

    permission_classes = (UserPermission, )


    @list_route(methods=['post'])
    def login(self, request, *args, **kwargs):
        user = authenticate(request, username=request.data['username'],
                         password=request.data['password'])

        data = {
            'token': user.auth_token.key,
            'is_staff': user.is_staff,
            'id': user.id,
        }

        return Response(data)

    @list_route()
    def vendors(self, request, *args, **kwargs):
        vendors = self.queryset.filter(is_superuser=False, is_staff=False)
        data = self.serializer_class(vendors, many=True)
        print(data)
        return Response(data.data)

