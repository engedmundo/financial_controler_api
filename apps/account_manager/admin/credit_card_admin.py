from django.contrib import admin

from apps.account_manager.models import CreditCard


@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "bank",
        "user",
        "payment_day",
        "expense_limit",
    ]
