from django_filters import rest_framework as filters
from .models import Parcel


class ParcelFilter(filters.FilterSet):
    parcel_type = filters.CharFilter(field_name='parcel_type__name', lookup_expr='exact')
    has_delivery_cost = filters.BooleanFilter(method='filter_has_delivery_cost')

    class Meta:
        model = Parcel
        fields = ['parcel_type', 'has_delivery_cost']

    def filter_has_delivery_cost(self, queryset, name, value):
        if value is True:
            return queryset.exclude(delivery_cost__isnull=True)
        elif value is False:
            return queryset.filter(delivery_cost__isnull=True)
        return queryset