from tests import APITestCase, MAINNET_VAL_IP
from tradehub.public_client import PublicClient


class TestTradeHubGetTokens(APITestCase):

    def setUp(self) -> None:
        self._client = PublicClient(MAINNET_VAL_IP)

    def test_get_tokens_structure(self):
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

        result: list = self._client.get_tokens()

        for token in result:
            self.assertDictStructure(expect, token)
