
from django.contrib import admin

from apps.financial_manager.models import Budget


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = [
        "category",
        "amount",
        "month",
        "year",
        "type",
        "description",
    ]

    list_filter = (
        "month",
        "year",
    )
