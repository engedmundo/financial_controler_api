from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.financial_manager.models import Transaction
from apps.financial_manager.serializers import TransactionSerializer
from apps.financial_manager.services.transaction_service import TransactionService


class TransactionViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        query_params = request.query_params
        filters = {"user": user}

        if query_params.get("start_date"):
            filters["date__gte"] = query_params["start_date"]

        if query_params.get("end_date"):
            filters["date__lte"] = query_params["end_date"]

        transactions = Transaction.objects.filter(**filters).order_by("date")

        service = TransactionService(transactions)
        summary = service.get_transactions_summary()
        report = TransactionSerializer(transactions, many=True).data
        response = {
            "transactions": report,
            "summary": summary,
        }

        return Response(response, status=status.HTTP_200_OK)
