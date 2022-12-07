from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, country, password=None):
        if not username:
            raise ValueError('username is required')
        if not first_name:
            raise ValueError('fisrt name is required')
        if not last_name:
            raise ValueError('last name is required')
        if not country:
            raise ValueError('Please choose a country')

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            country=country,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, country, password=None):
        user = self.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            country=country,
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    username = models.CharField(verbose_name=_(
        'username'), max_length=100, unique=True)
    first_name = models.CharField(verbose_name=_('first_name'), max_length=100)
    last_name = models.CharField(verbose_name=_('last_name'), max_length=100)
    country = CountryField(blank=True, blank_label='(select country)')
    balance = models.DecimalField(verbose_name=_(
        'balance'), default=0, max_digits=15, decimal_places=2)
    code_pin = models.CharField(max_length=4, default='0000')
    date_joined = models.DateTimeField(
        verbose_name=("date_joined"), auto_now_add=True)
    last_login = models.DateTimeField(verbose_name=_(
        'last login'), blank=True, null=True, auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'country']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def get_balance(self):
        return f'XAF {self.balance}'

    @property
    def get_country_currency(self):
        return 'XAF'
