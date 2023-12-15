from django.contrib import admin

from apps.account_manager.models import Bank


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "code",
    ]
