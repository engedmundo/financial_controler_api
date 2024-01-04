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
        transactions = Transaction.objects.filter(user=user)
        summary = TransactionService.get_transactions_summary(transactions)
        report = TransactionSerializer(transactions, many=True).data
        response = {
            "transactions": report,
            "summary": summary,
        }

        return Response(response, status=status.HTTP_200_OK)
