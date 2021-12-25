from decimal import Decimal
from typing import List, Sequence
from django.db import models, transaction
from dataclasses import dataclass
from django.db.models import Q

from django.db.models.aggregates import Sum
from bcoin.apps.coins.exceptions import (
    InvalidAmountException,
    WalletNotFoundException,
    YouTooBrokeException,
)

from bcoin.settings import COOL_GUY_AMOUNT, COOL_GUYS, STARTING_AMOUNT


class WalletManager(models.Manager):
    def create(self, **obj_data):
        wallet: Wallet = super().create(**obj_data)

        # Grab a new transaction id
        transaction_id = TransactionId.get_next()

        # Give the wallet the starting amount in a one-sided transaction
        amount = STARTING_AMOUNT

        # If the wallet is for someone on the cool guy list, give it the cool guy amount
        if wallet.discord_id in COOL_GUYS:
            amount = COOL_GUY_AMOUNT

        CoinTransfer.objects.create(
            wallet=wallet, transaction_id=transaction_id, amount=amount
        )

        return wallet


class Wallet(models.Model):
    """
    Wallet representing a single user
    """

    discord_id = models.CharField(max_length=50, null=False, unique=True)

    objects = WalletManager()

    @property
    def current_value(self):
        return CoinTransfer.objects.filter(wallet=self).aggregate(Sum("amount"))[
            "amount__sum"
        ]

    @property
    def transaction_history(self):
        transaction_ids = (
            CoinTransfer.objects.filter(wallet=self)
            .values_list("transaction_id", flat=True)
            .distinct()
        )

        transfers = CoinTransfer.objects.filter(
            transaction_id__in=transaction_ids
        ).order_by("transaction_id", "amount")

        transactions = Transaction.from_transfer_list(transfers)
        return transactions


class CoinTransfer(models.Model):
    """
    Ledger for coin transactions
    """

    wallet = models.ForeignKey(Wallet, null=False, on_delete=models.DO_NOTHING)
    transaction_id = models.IntegerField(null=False, db_index=True)
    amount = models.DecimalField(null=False, decimal_places=3, max_digits=12)
    date = models.DateTimeField(auto_now_add=True, null=False, db_index=True)

    @staticmethod
    def create_transaction(source, destination, amount):
        # Make sure both the source and destination wallets exist
        try:
            source_wallet = Wallet.objects.get(discord_id=source)
            destination_wallet = Wallet.objects.get(discord_id=destination)
        except Wallet.DoesNotExist as e:
            raise WalletNotFoundException(str(e))

        # Make sure the amount is not negative
        if amount <= 0:
            raise InvalidAmountException()

        # Make sure the source_wallet has the funds
        if source_wallet.current_value < amount:
            raise YouTooBrokeException(f"{source_wallet.discord_id} too broke for that")

        # Grab a new transaction id
        transaction_id = TransactionId.get_next()

        # Create two CoinTransfers, one debiting the source and one crediting the destination
        with transaction.atomic():
            source_ct = CoinTransfer.objects.create(
                wallet=source_wallet,
                amount=Decimal(amount * -1),
                transaction_id=transaction_id,
            )

            destination_ct = CoinTransfer.objects.create(
                wallet=destination_wallet,
                amount=Decimal(amount),
                transaction_id=transaction_id,
            )

        return Transaction(
            transaction_id=transaction_id,
            source_transfer=source_ct,
            destination_transfer=destination_ct,
        )


class TransactionId(models.Model):
    """
    Counter to generate transaction ids. The starter ID is created in a migration.
    """

    current_value = models.PositiveBigIntegerField(default=0)

    @classmethod
    def get_next(cls):
        with transaction.atomic():
            cls.objects.update(current_value=models.F("current_value") + 1)
            return cls.objects.values_list("current_value", flat=True)[0]


# POPO Models
@dataclass(frozen=True)
class Transaction:
    transaction_id: int
    source_transfer: CoinTransfer
    destination_transfer: CoinTransfer

    @staticmethod
    def from_transfer_list(transfers: Sequence[CoinTransfer]) -> List["Transaction"]:
        """
        transfers must be ordered by (transaction_id, amount) for this to work
        """
        transfers_by_transaction_id = {}
        for transfer in transfers:
            if transfer.transaction_id not in transfers_by_transaction_id:
                transfers_by_transaction_id[transfer.transaction_id] = []
            transfers_by_transaction_id[transfer.transaction_id].append(transfer)

        transactions = []
        for k, v in transfers_by_transaction_id.items():
            transaction = None
            if len(v) == 2:
                # Normal transaction
                transaction = Transaction(
                    transaction_id=k,
                    source_transfer=v[0],
                    destination_transfer=v[1],
                )
            elif len(v) == 1:
                # This is a new-account transaction
                transaction = Transaction(
                    transaction_id=k,
                    source_transfer=None,
                    destination_transfer=v[0],
                )
            transactions.append(transaction)

        return transactions
