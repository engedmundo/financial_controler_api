from django.views import View
from django.shortcuts import render



class TransactionsReportView(View):

    def post(self, request, *args, **kwargs):
        # "transactions/report.html"
        # Lógica para lidar com a solicitação POST aqui
        return render(request, 'transactions/report.html')