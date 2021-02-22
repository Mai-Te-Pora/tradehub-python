from tests import APITestCase, MAINNET_VAL_IP, WALLET_DEVEL
from tradehub.public_client import PublicClient


class TestTradeHubGetProfile(APITestCase):

    def setUp(self) -> None:
        self._client = PublicClient(MAINNET_VAL_IP)

    def test_get_profile_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            "address": str,
            "last_seen_block": str,
            "last_seen_time": str,
            "twitter": str,
            "username": str,
        }

        result: dict = self._client.get_profile(WALLET_DEVEL)

        self.assertDictStructure(expect, result)
