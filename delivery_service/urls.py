from django.urls import path
from django.contrib import admin
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from parcels.views import (
    RegisterParcelView,
    ParcelTypeListView,
    ParcelListView,
    TriggerDeliveryCostCalculation,    
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegisterParcelView.as_view(), name='register_parcel'),
    path('api/parcel-types/', ParcelTypeListView.as_view(), name='parcel_types'),
    path('api/parcels/', ParcelListView.as_view(), name='parcel_list'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/trigger-delivery-cost/', TriggerDeliveryCostCalculation.as_view(), name='trigger_delivery_cost'),
]