from django.db import models


class ParcelType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Parcel(models.Model):
    name = models.CharField(max_length=255)
    weight = models.FloatField()  # в кг
    parcel_type = models.ForeignKey(ParcelType, on_delete=models.CASCADE)
    content_cost = models.FloatField()  # в долларах
    delivery_cost = models.FloatField(null=True, blank=True)  # в рублях
    session_key = models.CharField(max_length=40)  # для отслеживания сессии
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name