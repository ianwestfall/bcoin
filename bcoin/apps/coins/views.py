from bcoin.apps.coins.models import CoinTransfer, Transaction, Wallet
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from bcoin.apps.coins.serializers import (
    CoinTransferSerializer,
    TransactionReadOnlySerializer,
    TransactionWriteSerializer,
    WalletSerializer,
)


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "discord_id"


class CoinTransferViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CoinTransfer.objects.all().order_by("-date")
    serializer_class = CoinTransferSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(["GET", "POST"])
@permission_classes([permissions.IsAuthenticated])
def list_transactions(request):
    if request.method == "GET":
        transfers = CoinTransfer.objects.order_by("transaction_id", "amount").all()

        transactions = Transaction.from_transfer_list(transfers)

        serializer = TransactionReadOnlySerializer(transactions, many=True)

        return Response(serializer.data)
    elif request.method == "POST":
        serializer = TransactionWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def view_transaction(request, transaction_id):
    transfers = (
        CoinTransfer.objects.filter(transaction_id=transaction_id)
        .order_by("amount")
        .all()
    )

    if len(transfers) <= 0:
        return Response(None, status=status.HTTP_404_NOT_FOUND)
    elif len(transfers) > 2:
        return Response(None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if len(transfers) == 1:
        transaction = Transaction(
            transaction_id=transaction_id,
            source_transfer=None,
            destination_transfer=transfers[0],
        )
    else:
        transaction = Transaction(
            transaction_id=transaction_id,
            source_transfer=transfers[0],
            destination_transfer=transfers[1],
        )

    serializer = TransactionReadOnlySerializer(transaction)
    return Response(serializer.data, status=status.HTTP_200_OK)
