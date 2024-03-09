from datetime import datetime, timedelta

from django.shortcuts import render
from django.views import View


class TransactionsReportView(View):
    def get(self, request, *args, **kwargs):
        today = datetime.now().date()

        start_date = request.GET.get("start_date", today - timedelta(days=30))
        end_date = request.GET.get("end_date", today)
        display_family = request.GET.get("display_family_check", False)

        print(start_date, end_date, display_family)
        print(today)

        context = {
            "start_date": start_date,
            "end_date": end_date,
            "display_family": display_family,
        }

        # "transactions/report.html"
        # Lógica para lidar com a solicitação POST aqui
        return render(
            request=request,
            template_name="transactions/report.html",
            context=context,
        )
