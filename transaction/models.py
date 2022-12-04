from django.db import models
from authentication.models import Account
# Create your models here.


class AbstractTransaction(models.Model):
    orderer = models.ForeignKey(
        Account, related_name="%(class)s_related", on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(
        max_digits=100, decimal_places=2, default=0.00)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.orderer.username}-{self.created}'


class Transaction(AbstractTransaction):
    receiver = models.ForeignKey(
        Account, related_name='receiver', on_delete=models.SET_NULL, null=True, blank=True)


class SelfTransaction(AbstractTransaction):
    withdrawed = models.BooleanField(default=False)
