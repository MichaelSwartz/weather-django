from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models


@python_2_unicode_compatible
class City(models.Model):
    display_name = models.CharField(max_length=200, null=False, unique=True)
    name = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=2, null=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.display_name


@python_2_unicode_compatible
class Subscriber(models.Model):
    email = models.EmailField(null=False, unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.email
