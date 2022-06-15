from django.contrib.auth.models import Permission as _Permission
from django.contrib.auth.models import User
from django.db import models


class Constellation(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class SolarSystem(models.Model):
    name = models.CharField(max_length=200, unique=True)
    constellation = models.ForeignKey("pochven.Constellation", on_delete=models.CASCADE)

    claimed_by = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True
    )
    home = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class Permission(_Permission):
    class Meta:
        proxy = True
