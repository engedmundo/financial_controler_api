from django.contrib.auth.models import User
from django.db import models

from apps.account_manager.models import Account, CreditCard
from apps.core.models.base_model import BaseModel
from apps.financial_manager.enums import FinancialTypeEnum
from apps.financial_manager.models.category import Category


class Transaction(BaseModel):
    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"

    user = models.ForeignKey(
        User,
        verbose_name="Usuário",
        on_delete=models.PROTECT,
    )
    account = models.ForeignKey(
        Account,
        verbose_name="Conta",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    credit_card = models.ForeignKey(
        CreditCard,
        verbose_name="Cartão de crédito",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Categoria",
        on_delete=models.PROTECT,
    )
    amount = models.DecimalField(
        verbose_name="Valor",
        decimal_places=2,
        max_digits=15,
    )
    date = models.DateField(
        verbose_name="Data da transação",
    )
    type = models.CharField(
        verbose_name="Tipo",
        max_length=255,
        choices=FinancialTypeEnum.choices,
    )
    description = models.CharField(
        verbose_name="Descrição",
        max_length=255,
    )

    def __str__(self) -> str:
        return str(self.description)
