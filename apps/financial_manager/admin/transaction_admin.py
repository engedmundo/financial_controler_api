from django.contrib import admin
from rangefilter.filters import DateRangeFilter

from apps.financial_manager.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "account",
        "credit_card",
        "category",
        "amount",
        "date",
        "type",
        "description",
    ]

    list_filter = (
        ("date", DateRangeFilter),
        "date",
    )
