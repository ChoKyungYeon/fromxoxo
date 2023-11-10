from django.db import models

from fromxoxo.choice import bankchoice
from fromxoxo.variables import bankdictionary


class Deposit(models.Model):
    bank = models.CharField(max_length=20, choices=bankchoice)
    accountnumber = models.CharField(max_length=30)
    depositor = models.CharField(max_length=20)

    def bankimage(self):
        return bankdictionary[self.bank] if self.bank else None

