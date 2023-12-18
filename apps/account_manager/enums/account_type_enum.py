from django.db import models


class AccountTypeEnum(models.TextChoices):
    CURRENT = "current", "Conta Corrente"
    SAVING = "saving", "Conta Poupança"
    INVESTMENT = "investment", "Conta Investimento"
