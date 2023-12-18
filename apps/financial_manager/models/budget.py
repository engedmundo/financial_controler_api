from django.contrib.auth.models import User
from django.db import models

from apps.core.models.base_model import BaseModel
from apps.financial_manager.enums import FinancialTypeEnum, MonthEnum
from apps.financial_manager.models.category import Category


class Budget(BaseModel):
    class Meta:
        verbose_name = "Orçamento"
        verbose_name_plural = "Orçamentos"

    user = models.ForeignKey(
        User,
        verbose_name="Usuário",
        on_delete=models.PROTECT,
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
    month = models.CharField(
        verbose_name="Mês de referência",
        max_length=255,
        choices=MonthEnum.choices,
    )
    year = models.IntegerField(
        verbose_name="Ano de referência",
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
