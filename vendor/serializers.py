from rest_framework import serializers
from vendor import models


class PopsicleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Popsicle


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        extra_kwargs = {"machine": {"write_only": True}}
        exclude = ('id',)


class StockSerializer(serializers.ModelSerializer):
    popsicle = PopsicleSerializer(read_only=True)

    class Meta:
        fields = "__all__"
        model = models.Stock


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.Purchase


class PopsicleEntrySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.PopsicleEntry


class PopsicleRemovalSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.PopsicleRemoval


class MachineSerializer(serializers.ModelSerializer):
    stocks = StockSerializer(many=True)
    locations = LocationSerializer(many=True, read_only=True)
    seller = serializers.SlugRelatedField(slug_field='username', queryset=models.User.objects.all())

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
        model = models.Machine


class UserSerializer(serializers.ModelSerializer):
    machines = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Machine.objects.all())

    class Meta:
        fields = ('id', 'machines', 'is_superuser', 'username', 'is_staff', )
        model = models.User
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if 'groups' in validated_data.keys():
            validated_data.pop('groups')
        if 'user_permissions' in validated_data.keys():
            validated_data.pop('user_permissions')

        user = models.User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
