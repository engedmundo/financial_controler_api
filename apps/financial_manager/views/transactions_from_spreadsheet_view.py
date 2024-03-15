from datetime import datetime, timedelta
from typing import Any

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from apps.financial_manager.services.google_spreadsheet_service import (
    GoogleSpreadsheetService,
)
from apps.financial_manager.services.transaction_service import (
    TransactionService,
)


class LoadTransactionsSpreadsheetView(View):
    def get(self, request):
        spreadsheet_service = GoogleSpreadsheetService()
        raw_sheet = spreadsheet_service.read_spreadsheet()
        transaction_service = TransactionService()
        
        family = transaction_service.get_family_members(request.user)
        family_members = transaction_service.get_family_members(family)
        accounts = transaction_service.get_accounts(request.user)
        credit_cards = transaction_service.get_credit_cards(request.user)
        categories = transaction_service.get_category_names()


        transactions = list()
        for row in raw_sheet[1:]:
            user_name = row[5]
            account_name = row[7]
            credit_card_name = row[6]
            category_name = row[3]

            print(user_name)

            transaction = {
                "user": family_members.get(user_name),
                "account": accounts.get(account_name),
                "credit_card_name": credit_cards.get(credit_card_name),
                "category_name": categories.get(category_name),
                "amount": row[2],
                "date": row[0],
                "type": row[4],
                "description": row[1],
            }
            transactions.append(transaction)

        print(transactions[0])

        if "HTTP_REFERER" in request.META:
            # Retorna/Redireciona para a página anterior
            return HttpResponseRedirect(request.META["HTTP_REFERER"])
        else:
            # Se o HTTP referer não estiver presente, redireciona para uma URL padrão
            return HttpResponseRedirect("/admin")


