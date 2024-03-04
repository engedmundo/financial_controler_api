from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FinancialManagerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.financial_manager"
    verbose_name = _("Gerenciamento Financeiro")
