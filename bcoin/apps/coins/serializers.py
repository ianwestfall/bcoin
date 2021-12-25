from django.contrib.auth.models import User, Group
from bcoin.apps.coins.models import CoinTransfer, Wallet
from bcoin.apps.coins.validators import is_greater_than_0
from rest_framework import serializers
from decimal import Decimal


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class CoinTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinTransfer
        fields = ["wallet", "transaction_id", "amount", "date"]
        depth = 1


class TransactionReadOnlySerializer(serializers.Serializer):
    transaction_id = serializers.IntegerField(read_only=True)
    source_transfer = CoinTransferSerializer()
    destination_transfer = CoinTransferSerializer()


class TransactionWriteSerializer(serializers.Serializer):
    source = serializers.CharField()
    destination = serializers.CharField()
    amount = serializers.DecimalField(decimal_places=3, max_digits=12)

    def save(self):
        CoinTransfer.create_transaction(
            source=self.data["source"],
            destination=self.data["destination"],
            amount=Decimal(self.data["amount"]),
        )


class WalletSerializer(serializers.ModelSerializer):
    transaction_history = TransactionReadOnlySerializer(many=True, read_only=True)

    class Meta:
        model = Wallet
        fields = ["id", "discord_id", "current_value", "transaction_history"]
        lookup_field = "discord_id"
