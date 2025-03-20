from celery.schedules import crontab


CELERY_BEAT_SCHEDULE = {
    'calculate-delivery-cost-every-5-minutes': {
        'task': 'parcels.tasks.calculate_delivery_cost',
        'schedule': crontab(minute='*/5'),
    },
}