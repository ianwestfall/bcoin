from decimal import Decimal
from typing import Sequence
from bcoin.apps.coins.models import Wallet
from bcoin.apps.coins.tests.factories import WalletFactory
from django.test import TestCase

from bcoin.settings import STARTING_AMOUNT


class TestWallet(TestCase):
    def test_give_weekly_coins_no_wallets(self):
        Wallet.give_weekly_coins()

        self.assertEqual(Wallet.objects.all().count(), 0)

    def test_give_weekly_coins(self):
        wallets: Sequence[Wallet] = WalletFactory.create_batch(5)

        Wallet.give_weekly_coins()

        for wallet in wallets:
            self.assertTrue(100 < wallet.current_value < 200)

    def test_give_free_coins(self):
        test_wallet: Wallet = WalletFactory.create()

        test_amount = Decimal("100.25")
        test_wallet.give_free_coins(test_amount)
        self.assertEqual(test_wallet.current_value, STARTING_AMOUNT + test_amount)

        test_amount_2 = Decimal("555")
        test_wallet.give_free_coins(test_amount_2)
        self.assertEqual(
            test_wallet.current_value, STARTING_AMOUNT + test_amount + test_amount_2
        )
