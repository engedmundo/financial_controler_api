from django.contrib import admin

from apps.account_manager.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "bank",
        "name",
        "agency",
        "number",
    ]
