from tests import APITestCase, DEVEL_AND_CO_SENTRY
from tradehub.public_client import PublicClient


class TestTradeHubGetTrades(APITestCase):

    def setUp(self) -> None:
        self._client = PublicClient(DEVEL_AND_CO_SENTRY)

    def test_get_trades_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            "id": str,
            "block_created_at": str,
            "taker_id": str,
            "taker_address": str,
            "taker_fee_amount": str,
            "taker_fee_denom": str,
            "taker_side": str,
            "maker_id": str,
            "maker_address": str,
            "maker_fee_amount": str,
            "maker_fee_denom": str,
            "maker_side": str,
            "market": str,
            "price": str,
            "quantity": str,
            "liquidation": str,
            "taker_username": str,
            "maker_username": str,
            "block_height": str,
        }

        result: list = self._client.get_trades()

        self.assertEqual(200, len(result), msg="Expected count(200) of trades are not returned.")

        for trade in result:
            self.assertDictStructure(expect, trade)
