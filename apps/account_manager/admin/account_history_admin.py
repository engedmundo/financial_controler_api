from django.contrib import admin
from rangefilter.filters import DateRangeFilter

from apps.account_manager.models import AccountHistory


@admin.register(AccountHistory)
class AccountHistoryAdmin(admin.ModelAdmin):
    def get_name(self, obj=None):
        return f"{self.user.first_name}"
    
    get_name.short_description = "Usuário"

    list_display = [
        "account",
        get_name,
        "date",
        "balance",
    ]

    list_filter = (
        ("date", DateRangeFilter),
        "date",
    )
