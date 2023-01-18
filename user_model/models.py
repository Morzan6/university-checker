from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

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
    username = models.CharField(unique=True,  verbose_name='username', max_length=20)
    email = models.EmailField(unique=True, null=True, verbose_name='email')
    

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

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = MyUserManager()

    def __str__(self):
        return str(self.email)

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username