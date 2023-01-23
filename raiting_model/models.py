from django.db import models

class Raiting(models.Model):
    users_name = models.CharField(max_length=25, verbose_name="users_name")
    rate = models.IntegerField(null=True, default=False)
    message  = models.CharField(max_length=200, null=True)
    service_name = models.CharField(max_length=200, null=True)
    