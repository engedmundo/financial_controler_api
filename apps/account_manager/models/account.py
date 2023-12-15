from django.contrib.auth.models import User
from django.db import models

from apps.account_manager.enums import AccountTypeEnum
from apps.account_manager.models.bank import Bank
from apps.core.models.base_model import BaseModel


class Account(BaseModel):
    class Meta:
        verbose_name = "Conta"
        verbose_name_plural = "Contas"

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
        verbose_name="Nome da conta",
        max_length=255,
    )
    agency = models.CharField(
        verbose_name="Agência",
        max_length=255,
    )
    number = models.CharField(
        verbose_name="Número da conta",
        max_length=255,
    )
    type = models.CharField(
        verbose_name="Tipo de conta",
        max_length=255,
        choices=AccountTypeEnum.choices,
    )

    def __str__(self) -> str:
        return str(self.name)