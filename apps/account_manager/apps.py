from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountManagerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.account_manager"
    verbose_name = _("Gerenciamento de Contas")
