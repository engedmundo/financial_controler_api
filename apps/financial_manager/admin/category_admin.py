from django.contrib import admin

from apps.financial_manager.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
    ]
