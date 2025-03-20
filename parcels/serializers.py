from rest_framework import serializers
from .models import Parcel, ParcelType

class ParcelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParcelType
        fields = ['id', 'name']

class ParcelSerializer(serializers.ModelSerializer):
    parcel_type = serializers.PrimaryKeyRelatedField(queryset=ParcelType.objects.all())
    delivery_cost = serializers.SerializerMethodField()

    class Meta:
        model = Parcel
        fields = ['id', 'name', 'weight', 'parcel_type', 'content_cost', 'delivery_cost']

    def get_delivery_cost(self, obj):
        return obj.delivery_cost if obj.delivery_cost is not None else "Не рассчитано"

    def validate_weight(self, value):
        if value <= 0:
            raise serializers.ValidationError("Вес должен быть положительным.")
        return value

    def validate_content_cost(self, value):
        if value < 0:
            raise serializers.ValidationError("Стоимость содержимого не может быть отрицательной.")
        return value