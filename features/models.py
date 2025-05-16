from django.db import models

class Feature(models.Model):
    name = models.CharField(max_length=200)
    feature_type = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    size = models.FloatField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

