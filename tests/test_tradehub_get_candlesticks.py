from tests import APITestCase, DEVEL_AND_CO_SENTRY
from tradehub.public_client import PublicClient


class TestTradeHubGetCandlesticks(APITestCase):

    def setUp(self) -> None:
        self._client = PublicClient(DEVEL_AND_CO_SENTRY)

    def test_get_candlesticks_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """
        expect: dict = {
            "id": int,
            "market": str,
            "time": str,
            "resolution": int,
            "open": str,
            "close": str,
            "high": str,
            "low": str,
            "volume": str,
            "quote_volume": str
        }

        granularity: int = 5  # 5 minutes
        market: str = "swth_eth1"
        open_time: int = 1610203000
        close_time: int = 1610203000 + granularity * 60  # add 5minutes

        result: list = self._client.get_candlesticks(market, granularity, open_time, close_time)

        # With 5 minutes granularity we expect just one candle
        self.assertEqual(1, len(result), msg="Expected count(1) of candlesticks are not returned.")

        for candle in result:
            self.assertDictStructure(expect, candle)
