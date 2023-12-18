from django.contrib.auth.models import User
from django.db import models

from apps.account_manager.models.bank import Bank
from apps.core.models.base_model import BaseModel


class CreditCard(BaseModel):
    class Meta:
        verbose_name = "Cartão de crédito"
        verbose_name_plural = "Cartões de crédito"

    user = models.ForeignKey(
        User,
        verbose_name="Usuário",
        on_delete=models.PROTECT,
    )
    bank = models.ForeignKey(
        Bank,
        verbose_name="Banco",
        on_delete=models.PROTECT,
    )
    name = models.CharField(
        verbose_name="Nome da cartão",
        max_length=255,
    )
    expense_limit = models.IntegerField(
        verbose_name="Limite de crédito",
        null=True,
        blank=True,
    )
    payment_day = models.IntegerField(
        verbose_name="Dia de vencimento",
    )

    def __str__(self) -> str:
        return str(self.name)
