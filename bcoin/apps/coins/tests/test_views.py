import base64
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import HTTP_HEADER_ENCODING, status
from rest_framework.test import APITestCase

from bcoin.apps.coins.tests.factories import WalletFactory


class TestWalletViewSet(APITestCase):
    def setUp(self) -> None:
        # Create a test user for auth
        test_user = "test_user"
        test_password = "password"

        User.objects.create_user(username=test_user, password=test_password)

        credentials = f"{test_user}:{test_password}"
        self.encoded_credentials = base64.b64encode(
            credentials.encode(HTTP_HEADER_ENCODING)
        ).decode(HTTP_HEADER_ENCODING)

        self.client.credentials(HTTP_AUTHORIZATION=f"Basic {self.encoded_credentials}")

    def tearDown(self) -> None:
        self.client.credentials()

    def test_users_can_have_periods_in_their_username(self):
        # Create a user with a period in their username
        test_discord_id = ".wushbacker#0"
        WalletFactory.create(discord_id=test_discord_id)

        # Make sure they can create and view a wallet
        url = reverse("wallet-detail", kwargs={"discord_id": test_discord_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
