from tests import APITestCase, mainnet_client, WALLET_DEVEL


class TestTradeHubGetProfile(APITestCase):

    def setUp(self) -> None:
        self._client = mainnet_client

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
