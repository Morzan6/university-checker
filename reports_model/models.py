from django.db import models

class Report(models.Model):
    users_name = models.CharField(max_length=25, verbose_name="users_name")
    types = models.CharField(max_length=200, null=True, default=False, verbose_name="types")
    message = models.CharField(max_length=200, null=True, default=False)
    is_moderated = models.BooleanField(default=False)