from django.contrib import admin

from apps.financial_manager.models import Budget


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = [
        "description",
        "category",
        "amount",
        "month",
        "year",
        "type",
    ]

    list_filter = (
        "month",
        "year",
        "category",
    )
