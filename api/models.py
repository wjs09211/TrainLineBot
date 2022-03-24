from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=30)
    code = models.IntegerField()

    class Meta:
        indexes = [models.Index(fields=['name'])]
        db_table = "station"
