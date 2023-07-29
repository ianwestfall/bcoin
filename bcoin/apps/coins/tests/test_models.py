from typing import Sequence
from bcoin.apps.coins.models import Wallet
from bcoin.apps.coins.tests.factories import WalletFactory
from django.test import TestCase


class TestWallet(TestCase):
    def test_give_weekly_coins_no_wallets(self):
        Wallet.give_weekly_coins()

        self.assertEqual(Wallet.objects.all().count(), 0)

    def test_give_weekly_coins(self):
        wallets: Sequence[Wallet] = WalletFactory.create_batch(100)

        Wallet.give_weekly_coins()

        for wallet in wallets:
            self.assertTrue(100 < wallet.current_value < 200)
