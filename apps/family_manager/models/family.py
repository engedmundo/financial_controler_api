from django.contrib.auth.models import User
from django.db import models

from apps.core.models.base_model import BaseModel


class Family(BaseModel):
    class Meta:
        verbose_name = "Família"
        verbose_name_plural = "Famílias"

    name = models.CharField(
        verbose_name="Nome da família",
        max_length=255,
    )
    members = models.ManyToManyField(
        User,
        verbose_name="Integrantes da família",
    )

    def __str__(self) -> str:
        return str(self.name)
