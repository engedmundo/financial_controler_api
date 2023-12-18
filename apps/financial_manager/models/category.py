from django.contrib.auth.models import User
from django.db import models

from apps.account_manager.models.bank import Bank
from apps.core.models.base_model import BaseModel


class Category(BaseModel):
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    user = models.ForeignKey(
        User,
        verbose_name="Usuário",
        on_delete=models.PROTECT,
    )
    name = models.CharField(
        verbose_name="Nome da categoria",
        max_length=255,
    )
    description = models.CharField(
        verbose_name="Descrição",
        max_length=255,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return str(self.name)
