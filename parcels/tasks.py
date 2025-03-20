import logging
import requests
from celery import shared_task
from django.core.cache import cache
from .models import Parcel


logger = logging.getLogger('parcels')

EXCHANGE_RATE_CACHE_KEY = 'usd_to_rub_rate'
EXCHANGE_RATE_URL = 'https://www.cbr-xml-daily.ru/daily_json.js'


def get_usd_to_rub_rate():
    """Получение курса доллара к рублю с кэшированием в Redis."""
    cached_rate = cache.get(EXCHANGE_RATE_CACHE_KEY)
    if cached_rate:
        return cached_rate

    try:
        response = requests.get(EXCHANGE_RATE_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        rate = data['Valute']['USD']['Value']
        cache.set(EXCHANGE_RATE_CACHE_KEY, rate, timeout=86400)
        return rate
    except (requests.RequestException, KeyError) as e:
        return None


@shared_task
def calculate_delivery_cost():
    """Задача для расчета стоимости доставки для необработанных посылок."""
    unprocessed_parcels = Parcel.objects.filter(delivery_cost__isnull=True)
    if not unprocessed_parcels.exists():
        return "No parcels to process."

    usd_to_rub = get_usd_to_rub_rate()
    if not usd_to_rub:
        logger.error("Failed to fetch USD to RUB exchange rate.")
        return "Failed to fetch exchange rate."

    for parcel in unprocessed_parcels:
        delivery_cost = (parcel.weight * 0.5 + parcel.content_cost * 0.01) * usd_to_rub
        parcel.delivery_cost = delivery_cost
        parcel.save(update_fields=['delivery_cost'])
        logger.info(f"Calculated delivery cost for parcel ID {parcel.id}: {delivery_cost} RUB")

    return f"Processed {unprocessed_parcels.count()} parcels."