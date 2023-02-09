from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class MyUserManager(BaseUserManager):
    def _create_user(self,username, email, password, **kwargs):    
        if not email:
            raise ValueError('Нужно указать почту')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,username, email, password):
        return self._create_user(username=username, email=email, password=password, is_staff=True, is_superuser=True, is_active=True)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True,  verbose_name='username', max_length=20, null=True)
    email = models.EmailField(unique=True, null=True, verbose_name='email')
    subscribes = models.CharField(null=True, max_length=9999)
    tgid = models.CharField(unique=True, null=True, max_length=50)
    

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    
    is_confirmed = models.BooleanField(
        _('confirmed'),
        default=False,
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = MyUserManager()

    def __str__(self):
        return str(self.username)

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

class Service(models.Model):
    name = models.CharField(max_length=25, db_index=True, unique=True, verbose_name="name")
    url = models.URLField(max_length=25, unique=True)
    status = models.CharField(max_length=999999, default = None,null=True)
    reports = models.CharField(max_length=999999, default = None,null=True)
    time = models.CharField(max_length=999999, default = None,null=True)  
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    image = models.FileField(null=True)
    abbreviation = models.CharField(unique=True, max_length=255, null=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('service', kwargs={'post_slug': self.slug})

class Report(models.Model):
    users_name = models.CharField(max_length=25, verbose_name="users_name", unique=False)
    types = models.CharField(max_length=200, null=True,  verbose_name="types", unique=False)
    message = models.CharField(max_length=200, null=True, unique=False)
    service_slug = models.SlugField(max_length=255, null=True, unique=False)
    is_moderated = models.BooleanField(default=False, unique=False)
    time = models.CharField(max_length=200, null=True,  verbose_name="time", unique=False)


class Raiting(models.Model):
    users_name = models.CharField(max_length=25, verbose_name="users_name")
    rate = models.IntegerField(null=True, default=False)
    message  = models.CharField(max_length=200, null=True)
    service_name = models.CharField(max_length=200, null=True)
    