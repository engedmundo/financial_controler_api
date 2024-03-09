from django.contrib import admin
from django.contrib.auth.models import User

from apps.account_manager.models import CreditCard


@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    def get_name(self, obj=None):
        return f"{self.user.first_name}"

    get_name.short_description = "Usuário"

    list_display = [
        "name",
        get_name,
        "bank",
        "payment_day",
        "expense_limit",
    ]
