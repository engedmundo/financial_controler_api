from django.contrib import admin

from apps.account_manager.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    def get_name(self, obj=None):
        return f"{self.user.first_name}"

    get_name.short_description = "Usuário"

    list_display = [
        "name",
        get_name,
        "bank",
        "agency",
        "number",
    ]
