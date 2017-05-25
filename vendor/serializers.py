from rest_framework import serializers
from vendor.models import Popsicle, Machine, Location, Stock, Transaction, User


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
    popsicle = serializers.SlugRelatedField(
        slug_field='flavor',
        queryset=Popsicle.objects.all()
    )
    class Meta:
        fields = "__all__"
        model = Stock


# class TransactionSerializer(serializers.ModelSerializer):
#     def validate_amount(self, value):
#         if value > 0:
#             return value
#         else:
#             raise serializers.ValidationError("Amount of popsicles MUST be greater than zero.")

#     def to_representation(self, obj):
#         total = (obj.amount * int(obj.popsicle.price))/100 # Price is in cents
#         data = {
#             "is_purchase": obj.is_purchase,
#             "amount": obj.amount,
#             "total": total
#         }
#         return data

#     class Meta:
#         fields = "__all__"
#         model = Transaction


class MachineSerializer(serializers.ModelSerializer):
    stocks = StockSerializer(many=True, read_only=True)
    locations = LocationSerializer(many=True, read_only=True)

    def to_representation(self, obj):
        data = super().to_representation(obj)
        machine = dict(data)
        if len(data["locations"]) > 0:
            machine["location"] = data["locations"][-1]
        else:
            machine["location"] = None

        machine.pop("locations")
        return machine

    class Meta:
        fields = "__all__"
        model = Machine


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = User
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user