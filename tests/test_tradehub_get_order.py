from tests import APITestCase, DEVEL_AND_CO_SENTRY
from tradehub.public_client import PublicClient


class TestTradeHubGetOrder(APITestCase):

    def setUp(self) -> None:
        self._client = PublicClient(DEVEL_AND_CO_SENTRY)

    def test_get_get_order_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            "order_id": str,
            "block_height": int,
            "triggered_block_height": int,
            "address": str,
            "market": str,
            "side": str,
            "price": str,
            "quantity": str,
            "available": str,
            "filled": str,
            "order_status": str,
            "order_type": str,
            "initiator": str,
            "time_in_force": str,
            "stop_price": str,
            "trigger_type": str,
            "allocated_margin_denom": str,
            "allocated_margin_amount": str,
            "is_liquidation": bool,
            "is_post_only": bool,
            "is_reduce_only": bool,
            "type": str,
            "block_created_at": str,
            "username": str,
            "id": str
        }

        result: dict = self._client.get_order("4F54D2AE0D793F833806109B4278335BF3D392D4096B682B9A27AF9F8A8BCA58")

        self.assertDictStructure(expect, result)
