from django.contrib import admin

from apps.account_manager.models import AccountHistory


@admin.register(AccountHistory)
class AccountHistoryAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "account",
        "date",
        "balance",
    ]
