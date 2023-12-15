from django.contrib import admin

from apps.family_manager.models import Family


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]
