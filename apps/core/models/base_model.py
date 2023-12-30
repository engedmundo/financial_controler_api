from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name="Criação",
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        verbose_name="Atualização",
        auto_now=True,
        editable=False,
    )

    class Meta:
        abstract = True
