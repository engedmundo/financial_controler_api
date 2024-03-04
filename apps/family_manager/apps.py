from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FamilyManagerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.family_manager"
    verbose_name = _("Gerenciamento de Família")
