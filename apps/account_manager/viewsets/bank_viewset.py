from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.account_manager.models import Bank
from apps.account_manager.seralizers import BankSerializer


class BankViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        banks = Bank.objects.all()
        serializer = BankSerializer(banks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)