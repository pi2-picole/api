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
    stocks = StockSerializer(many=True, read_only=True)
    locations = LocationSerializer(many=True, read_only=True)
    seller = serializers.SlugRelatedField(slug_field='username',
                                          # read_only=True
                                          queryset=models.User.objects.all())

    def create(self, validated_data):
        user = validated_data.pop('seller')
        machine = models.Machine(**validated_data)
        machine.seller_id = user.id
        machine.save()
        return machine

    def update(self, instance, validated_data):
        if 'is_active' in validated_data.keys():
            instance.is_active = validated_data['is_active']
        if 'ip' in validated_data.keys():
            instance.ip = validated_data['ip']
        if 'label' in validated_data.keys():
            instance.label = validated_data['label']

        if 'seller' in validated_data.keys():
            seller = validated_data.pop('seller')
            instance.seller_id = seller.id

        instance.save()
        return instance


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
    machines = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        fields = ('id', 'machines', 'is_superuser', 'username', 'is_staff', 'email', 'password')
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
