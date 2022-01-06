from django.db import models


class RoutingOptionsModel(models.Model):
    """Model for the request payload of the /routing endpoint."""

    origin = models.CharField(max_length=3)
    destination = models.CharField(max_length=3)
    cutoff = models.IntegerField(blank=True)
    plus_on_min_length = models.IntegerField(blank=True)
    plus_on_min_cost = models.FloatField(blank=True)

    class Meta:
        managed = False
