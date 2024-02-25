from django.db import models


class Push(models.Model):
    name = models.CharField()
    email = models.EmailField()
