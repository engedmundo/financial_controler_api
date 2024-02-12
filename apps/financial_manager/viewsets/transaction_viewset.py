from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.account_manager.models import Account, CreditCard
from apps.family_manager.models import Family
from apps.financial_manager.models import Category, Transaction
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

    def post(self, request):
        user = request.user
        account_id = request.data.get("account")
        credit_card_id = request.data.get("credit_card")
        category_id = request.data.get("category")

        family = Family.objects.filter(
            members=user,
        ).first()

        transaction_data = {
            "user": user,
            "amount": request.data.get("amount"),
            "date": request.data.get("date"),
            "type": request.data.get("type"),
            "description": request.data.get("description"),
        }

        if account_id:
            account = Account.objects.filter(
                id=account_id,
                user=user,
            ).first()

            if not account:
                return Response(
                    {"error": "Conta não encontrada"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            transaction_data["account"] = account

        if credit_card_id:
            credit_card = CreditCard.objects.filter(
                id=credit_card_id,
                user=user,
            ).first()

            if not credit_card:
                return Response(
                    {"error": "Cartão de crédito não encontrado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            transaction_data["credit_card"] = credit_card

        if category_id:
            category = Category.objects.filter(
                id=category_id,
                user__in=family.members.all(),
            ).first()

            if not category:
                return Response(
                    {"error": "Categoria não encontrada"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            transaction_data["category"] = category

        transaction, created = Transaction.objects.update_or_create(
            **transaction_data,
        )

        response_data = TransactionSerializer(transaction).data

        if created:
            return Response(
                {
                    "message": "Transação criada com sucesso",
                    "transaction": response_data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "message": "Transação atualizada com sucesso",
                "transaction": response_data,
            },
            status=status.HTTP_200_OK,
        )
