from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.financial_manager.services import TransactionCSVService


class TransactionCSVViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data
        if not data.get("csv_file"):
            response = {"error": "Um arquivo *.csv deve ser enviado"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        service = TransactionCSVService(user, data)
        transactions_df = service.get_file_content_df()
        transactions = service.treat_content_df(transactions_df)
        response = service.create_or_update_transactions(transactions)
        return Response(response, status=status.HTTP_200_OK)
