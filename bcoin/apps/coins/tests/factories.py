from bcoin.apps.coins.models import Wallet
from factory.django import DjangoModelFactory
import factory


class WalletFactory(DjangoModelFactory):
    discord_id = factory.Faker("user_name")

    class Meta:
        model = Wallet
