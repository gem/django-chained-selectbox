from django.db import models


class StandardModel(models.Model):
    name = models.CharField(max_length=255)

    field_one = models.CharField(max_length=255)
    field_two = models.CharField(max_length=255)
    field_three = models.CharField(max_length=255)

    def __unicode__(self):
        return (self.name)
