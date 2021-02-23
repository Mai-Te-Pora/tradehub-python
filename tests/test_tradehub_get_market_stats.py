from tests import APITestCase, mainnet_client


class TestTradeHubGetMarketStats(APITestCase):

    def setUp(self) -> None:
        self._client = mainnet_client

    def test_get_market_stats_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            "day_high": str,
            "day_low": str,
            "day_open": str,
            "day_close": str,
            "day_volume": str,
            "day_quote_volume": str,
            "index_price": str,
            "mark_price": str,
            "last_price": str,
            "market": str,
            "market_type": str,
            "open_interest": str
        }

        result: list = self._client.get_market_stats()

        for market in result:
            self.assertDictStructure(expect, market)
