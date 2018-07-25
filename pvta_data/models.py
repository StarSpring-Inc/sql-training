from django.db import models

class Route(models.Model):
    id = models.IntegerField(primary_key=True)
    short_name = models.CharField(max_length=5, blank=False)
    long_name = models.CharField(max_length=100)
    route_abbreviation = models.CharField(max_length=5)
    color = models.CharField(max_length=6)

class Stop(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    longitude = models.DecimalField(max_digits=8, decimal_places=6)
    is_time_point = models.BooleanField(default=False)

class Departure(models.Model):
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE, blank=False)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, blank=False)
    direction = models.CharField(max_length=50)
    is_done = models.BooleanField(default=False)
    sdt = models.TimeField(blank=False)
    edt = models.TimeField()
    headsign = models.CharField(max_length=100)