from django.db import models


class FinancialTypeEnum(models.TextChoices):
    EXPENSE = "expense", "Despesa"
    RECEIPT = "receipt", "Receita"