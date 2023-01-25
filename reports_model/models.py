from django.db import models

class Report(models.Model):
    users_name = models.CharField(max_length=25, verbose_name="users_name", unique=False)
    types = models.CharField(max_length=200, null=True,  verbose_name="types", unique=False)
    message = models.CharField(max_length=200, null=True, unique=False)
    service_slug = models.SlugField(max_length=255, null=True, unique=False)
    is_moderated = models.BooleanField(default=False, unique=False)