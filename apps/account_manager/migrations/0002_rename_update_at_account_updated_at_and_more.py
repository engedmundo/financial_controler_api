# Generated by Django 4.2 on 2023-12-30 14:53

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("account_manager", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="account",
            old_name="update_at",
            new_name="updated_at",
        ),
        migrations.RenameField(
            model_name="accounthistory",
            old_name="update_at",
            new_name="updated_at",
        ),
        migrations.RenameField(
            model_name="bank",
            old_name="update_at",
            new_name="updated_at",
        ),
        migrations.RenameField(
            model_name="creditcard",
            old_name="update_at",
            new_name="updated_at",
        ),
    ]