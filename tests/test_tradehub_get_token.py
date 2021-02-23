from tests import APITestCase, mainnet_client


class TestTradeHubGetToken(APITestCase):

    def setUp(self) -> None:
        self._client = mainnet_client

    def test_get_token_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            "name": str,
            "symbol": str,
            "denom": str,
            "decimals": int,
            "blockchain": str,
            "chain_id": int,
            "asset_id": str,
            "is_active": bool,
            "is_collateral": bool,
            "lock_proxy_hash": str,
            "delegated_supply": str,
            "originator": str
        }

        result: dict = self._client.get_token("swth")

        self.assertDictStructure(expect, result)
