# Generated by Django 5.0 on 2023-12-15 16:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Bank",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Criação"),
                ),
                (
                    "update_at",
                    models.DateTimeField(auto_now=True, verbose_name="Atualização"),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Nome do banco"),
                ),
                (
                    "code",
                    models.CharField(max_length=255, verbose_name="Código do banco"),
                ),
            ],
            options={
                "verbose_name": "Banco",
                "verbose_name_plural": "Bancos",
            },
        ),
        migrations.CreateModel(
            name="Account",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Criação"),
                ),
                (
                    "update_at",
                    models.DateTimeField(auto_now=True, verbose_name="Atualização"),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Nome da conta"),
                ),
                ("agency", models.CharField(max_length=255, verbose_name="Agência")),
                (
                    "number",
                    models.CharField(max_length=255, verbose_name="Número da conta"),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("current", "Conta Corrente"),
                            ("saving", "Conta Poupança"),
                            ("investment", "Conta Investimento"),
                        ],
                        max_length=255,
                        verbose_name="Tipo de conta",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Usuário",
                    ),
                ),
                (
                    "bank",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="account_manager.bank",
                        verbose_name="Banco",
                    ),
                ),
            ],
            options={
                "verbose_name": "Conta",
                "verbose_name_plural": "Contas",
            },
        ),
        migrations.CreateModel(
            name="AccountHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Criação"),
                ),
                (
                    "update_at",
                    models.DateTimeField(auto_now=True, verbose_name="Atualização"),
                ),
                ("date", models.DateField(verbose_name="Data do saldo")),
                (
                    "balance",
                    models.DecimalField(
                        decimal_places=2, max_digits=15, verbose_name="Saldo do dia"
                    ),
                ),
                (
                    "account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="account_manager.account",
                        verbose_name="Banco",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Usuário",
                    ),
                ),
            ],
            options={
                "verbose_name": "Histórico de conta",
                "verbose_name_plural": "Históricos de contas",
            },
        ),
        migrations.CreateModel(
            name="CreditCard",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Criação"),
                ),
                (
                    "update_at",
                    models.DateTimeField(auto_now=True, verbose_name="Atualização"),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Nome da cartão"),
                ),
                (
                    "expense_limit",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Limite de crédito"
                    ),
                ),
                ("payment_day", models.IntegerField(verbose_name="Dia de vencimento")),
                (
                    "bank",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="account_manager.bank",
                        verbose_name="Banco",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Usuário",
                    ),
                ),
            ],
            options={
                "verbose_name": "Cartão de crédito",
                "verbose_name_plural": "Cartões de crédito",
            },
        ),
    ]
