from datetime import datetime, timedelta

from django.shortcuts import render
from django.views import View

from apps.financial_manager.services.transaction_service import (
    TransactionService,
)


class TransactionsReportView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        filter_params = self.get_filter_params(request)
        service = TransactionService()

        transactions = service.get_transactions_queryset(
            filter_params=filter_params,
            user=user,
        )
        summary = service.get_transactions_summary(transactions)
        # precisa renderizar o resumo na tela
        context = {
            **filter_params,
            "transactions": transactions,
            "summary": summary,
        }

        return render(
            request=request,
            template_name="transactions/report.html",
            context=context,
        )

    def get_filter_params(self, request) -> dict:
        today = datetime.now().date()

        start_date = request.GET.get("start_date", today - timedelta(days=30))
        if type(start_date) == str:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")

        end_date = request.GET.get("end_date", today)
        if type(end_date) == str:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

        display_family = request.GET.get("display_family", "False")
        display_family = display_family.lower() == "true"

        display_receipt = (
            False if not request.GET.get("display_receipt") else True
        )

        display_expense = (
            False if not request.GET.get("display_expense") else True
        )

        return {
            "start_date": start_date,
            "end_date": end_date,
            "display_family": display_family,
            "display_receipt": display_receipt,
            "display_expense": display_expense,
        }
