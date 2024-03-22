import io

import pandas as pd
from django.contrib.auth.models import User

from apps.account_manager.models import Account, CreditCard
from apps.family_manager.models import Family
from apps.financial_manager.models import Category, Transaction


class TransactionCSVService:
    def __init__(self, user: User, request_data: dict) -> None:
        self.user = user
        self.request_data = request_data
        self.account = self._get_account()
        self.credit_card = self._get_credit_card()
        self.family = self._get_family()
        self.categories_map = self._get_categories_map()

    def _get_account(self) -> Account:
        return Account.objects.filter(
            user=self.user,
            id=self.request_data.get("account"),
        ).first()

    def _get_credit_card(self) -> CreditCard:
        return CreditCard.objects.filter(
            user=self.user,
            id=self.request_data.get("credit_card"),
        ).first()

    def _get_family(self) -> Family:
        return Family.objects.filter(members=self.user).first()

    def _get_categories_map(self) -> dict:
        users_filter = list()
        if self.family:
            users_filter.extend(self.family.members.all())
        else:
            users_filter.append(self.user)

        categories = Category.objects.filter(user__in=users_filter)
        categories_map = {category.name: category for category in categories}
        return categories_map

    def get_file_content_df(self) -> pd.DataFrame:
        file_content = io.BytesIO(self.request_data["csv_file"].read())
        return pd.read_csv(file_content, sep=",")

    def treat_content_df(self, transactions_df: pd.DataFrame) -> list:
        # transform date to iso format
        transactions_df["date"] = pd.to_datetime(
            transactions_df["date"], format="%d/%m/%Y"
        )
        transactions_df["date"] = transactions_df["date"].dt.strftime(
            "%Y-%m-%d"
        )

        # convert amount to decimal value
        transactions_df["amount"] = transactions_df["amount"].str.replace(
            ".", ""
        )
        transactions_df["amount"] = transactions_df["amount"].str.replace(
            ",", "."
        )
        transactions_df["amount"] = pd.to_numeric(
            transactions_df["amount"], errors="coerce"
        )

        # create user column
        transactions_df["user"] = self.user

        # create account column if exists
        if self.account:
            transactions_df["account"] = self.account

        # create credit_card column if exists
        if self.credit_card:
            transactions_df["credit_card"] = self.credit_card

        return transactions_df.to_dict(orient="records")

    def create_or_update_transactions(self, transactions: list) -> dict:
        qtt_transactions_saved = 0
        failed_registers = []

        for transaction in transactions:
            actual_category = self.categories_map.get(transaction["category"])
            transaction["category"] = actual_category

            try:
                obj, created = Transaction.objects.update_or_create(
                    date=transaction["date"],
                    user=transaction["user"],
                    amount=transaction["amount"],
                    description=transaction["description"],
                    defaults=transaction,
                )
                qtt_transactions_saved += 1

            except Exception as err:
                failed_transaction = {
                    "date": transaction["date"],
                    "description": transaction["description"],
                    "amount": transaction["amount"],
                    "error": str(err),
                }
                failed_registers.append(failed_transaction)
                continue

        return {
            "saved_registers": qtt_transactions_saved,
            "failed_registers": failed_registers,
        }
