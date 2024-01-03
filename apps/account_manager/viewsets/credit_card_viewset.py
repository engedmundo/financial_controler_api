from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.account_manager.models import CreditCard
from apps.account_manager.seralizers import CreditCardSerializer
from rest_framework.permissions import IsAuthenticated


class CreditCardViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cards = CreditCard.objects.filter(user=user)
        serializer = CreditCardSerializer(cards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
