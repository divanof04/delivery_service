import logging
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Parcel, ParcelType
from .serializers import ParcelSerializer, ParcelTypeSerializer
from .filters import ParcelFilter
from .tasks import calculate_delivery_cost


logger = logging.getLogger('parcels')


class RegisterParcelView(generics.CreateAPIView):
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer

    @extend_schema(
        request=ParcelSerializer,
        responses={201: ParcelSerializer},
        description="Регистрация новой посылки. Возвращает уникальный ID посылки."
    )
    def post(self, request, *args, **kwargs):
        logger.debug(f"Received request to register parcel: {request.data}")
        try:
            response = super().post(request, *args, **kwargs)
            logger.info(f"Parcel registered successfully with ID: {response.data['id']}")
            return response
        except Exception as e:
            logger.error(f"Error registering parcel: {str(e)}")
            return Response({"error": "Failed to register parcel"}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        session_key = self.request.session.session_key
        if not session_key:
            self.request.session.create()
            session_key = self.request.session.session_key
        serializer.save(session_key=session_key)
        return Response({"parcel_id": serializer.instance.id}, status=status.HTTP_201_CREATED)


class ParcelTypeListView(generics.ListAPIView):
    queryset = ParcelType.objects.all()
    serializer_class = ParcelTypeSerializer

    @extend_schema(description="Получение списка всех типов посылок с их ID.")
    def get(self, request, *args, **kwargs):
        logger.debug("Fetching parcel types")
        return super().get(request, *args, **kwargs)


class ParcelListView(generics.ListAPIView):
    serializer_class = ParcelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ParcelFilter

    @extend_schema(
        parameters=[
            OpenApiParameter(name='parcel_type', type=str, description='Фильтр по типу посылки'),
            OpenApiParameter(name='has_delivery_cost', type=bool, description='Фильтр по наличию стоимости доставки'),
        ],
        description="Получение списка посылок пользователя с пагинацией и фильтрацией."
    )
    def get(self, request, *args, **kwargs):
        logger.debug(f"Fetching parcels with filters: {request.query_params}")
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error fetching parcels: {str(e)}")
            return Response({"error": "Failed to fetch parcels"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_queryset(self):
        session_key = self.request.session.session_key
        if not session_key:
            logger.warning("No session key found, returning empty queryset")
            return Parcel.objects.none()
        queryset = Parcel.objects.filter(session_key=session_key)
        parcel_type = self.request.query_params.get('parcel_type', None)
        has_delivery_cost = self.request.query_params.get('has_delivery_cost', None)
        if parcel_type:
            queryset = queryset.filter(parcel_type__name=parcel_type)
        if has_delivery_cost == 'true':
            queryset = queryset.exclude(delivery_cost__isnull=True)
        elif has_delivery_cost == 'false':
            queryset = queryset.filter(delivery_cost__isnull=True)
        return queryset



class TriggerDeliveryCostCalculation(APIView):
    permission_classes = [AllowAny]

    @extend_schema(description="Ручной запуск расчета стоимости доставки.")
    def post(self, request, *args, **kwargs):
        logger.info("Triggering delivery cost calculation task")
        try:
            calculate_delivery_cost.delay()
            logger.info("Task successfully triggered")
            return Response({"message": "Task triggered"}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            logger.error(f"Failed to trigger task: {str(e)}")
            return Response({"error": f"Failed to trigger task: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
