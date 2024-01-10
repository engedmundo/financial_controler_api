from django.db import models

from apps.core.models.base_model import BaseModel


class Bank(BaseModel):
    class Meta:
        verbose_name = "Banco"
        verbose_name_plural = "Bancos"

    name = models.CharField(
        verbose_name="Nome do banco",
        max_length=255,
    )
    code = models.CharField(
        verbose_name="Código do banco",
        max_length=255,
    )

    def __str__(self) -> str:
        return str(self.name)
