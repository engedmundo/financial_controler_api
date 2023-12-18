from django.contrib.auth.models import User
from django.db import models

from apps.account_manager.models.account import Account
from apps.core.models.base_model import BaseModel


class AccountHistory(BaseModel):
    class Meta:
        verbose_name = "Histórico de conta"
        verbose_name_plural = "Históricos de contas"

    user = models.ForeignKey(
        User,
        verbose_name="Usuário",
        on_delete=models.PROTECT,
    )
    account = models.ForeignKey(
        Account,
        verbose_name="Banco",
        on_delete=models.PROTECT,
    )
    date = models.DateField(
        verbose_name="Data do saldo",
    )
    balance = models.DecimalField(
        verbose_name="Saldo do dia",
        decimal_places=2,
        max_digits=15,
    )

    def __str__(self) -> str:
        return str(self.account)
