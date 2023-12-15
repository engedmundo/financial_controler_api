
from django.contrib import admin

from apps.financial_manager.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "account",
        "credit_card",
        "category",
        "amount",
        "date",
        "type",
        "description",
    ]
