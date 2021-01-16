from tests import APITestCase, DEVEL_AND_CO_SENTRY
from tradehub.public_client import PublicClient


class TestTradeHubGetMarkets(APITestCase):

    def setUp(self) -> None:
        self._client = PublicClient(DEVEL_AND_CO_SENTRY)

    def test_get_markets_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """
        expect: dict = {
            "type": str,
            "name": str,
            "display_name": str,
            "description": str,
            "market_type": str,
            "base": str,
            "base_name": str,
            "base_precision": int,
            "quote": str,
            "quote_name": str,
            "quote_precision": int,
            "lot_size": str,
            "tick_size": str,
            "min_quantity": str,
            "maker_fee": str,
            "taker_fee": str,
            "risk_step_size": str,
            "initial_margin_base": str,
            "initial_margin_step": str,
            "maintenance_margin_ratio": str,
            "max_liquidation_order_ticket": str,
            "max_liquidation_order_duration": int,
            "impact_size": str,
            "mark_price_band": int,
            "last_price_protected_band": int,
            "index_oracle_id": str,
            "expiry_time": str,
            "is_active": bool,
            "is_settled": bool,
            "closed_block_height": int,
            "created_block_height": int
        }

        result: list = self._client.get_markets()

        for market in result:
            self.assertDictStructure(expect, market)