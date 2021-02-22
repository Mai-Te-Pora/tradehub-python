import asyncio
from typing import Optional

from tests import APITestCase, MAINNET_VAL_IP, WALLET_SWTH_ETH1_AMM, WEBSOCKET_TIMEOUT_GET_REQUEST
from tradehub.websocket_client import DemexWebsocket


class TestWSGetOpenOrders(APITestCase):

    def test_get_open_orders_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """
        expect: dict = {
            "id": str,
            "result": [
                {
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
                    "id": str,
                }
            ]
        }

        # connect to websocket
        client = DemexWebsocket(f"ws://{MAINNET_VAL_IP}:5000/ws")
        # little work around to save the response
        self.response: Optional[dict] = None

        async def on_connect():
            await client.get_open_orders('order_history', WALLET_SWTH_ETH1_AMM)

        async def on_message(message: dict):
            # save response into self
            self.response = message
            await client.disconnect()

        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait_for(client.connect(on_connect_callback=on_connect,
                                                                    on_receive_message_callback=on_message),
                                                     WEBSOCKET_TIMEOUT_GET_REQUEST))
        except asyncio.TimeoutError:
            raise TimeoutError("Test did not complete in time.")

        if not self.response:
            raise RuntimeError("Did not receive a response.")

        self.assertDictStructure(expect, self.response)
