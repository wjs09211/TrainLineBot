from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=32)
    code = models.IntegerField()

    class Meta:
        indexes = [models.Index(fields=['name'])]
        db_table = "station"


class Task(models.Model):
    line_id = models.UUIDField()
    status = models.CharField(max_length=32)

    class Meta:
        db_table = "task"
