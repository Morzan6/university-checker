from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=25, verbose_name="name")
    url = models.URLField(max_length=25)
    status = models.CharField(max_length=999999, default = None,null=True)
    reports = models.CharField(max_length=999999, default = None,null=True)
    time = models.CharField(max_length=999999, default = None,null=True)  

    def __str__(self):
        return str(self.name)
