from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=25, db_index=True, unique=True, verbose_name="name")
    url = models.URLField(max_length=25, unique=True)
    status = models.CharField(max_length=999999, default = None,null=True)
    reports = models.CharField(max_length=999999, default = None,null=True)
    time = models.CharField(max_length=999999, default = None,null=True)  
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return str(self.name)
