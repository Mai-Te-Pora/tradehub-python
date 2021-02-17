import asyncio
import concurrent
from typing import Optional

from tests import APITestCase, DEVEL_AND_CO_SENTRY, WEBSOCKET_TIMEOUT_GET_REQUEST
from tradehub.websocket_client import DemexWebsocket


class TestWSGetRecentTrades(APITestCase):

    def test_get_recent_trades_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """
        expect: dict = {
            "id": str,
            "sequence_number": int,
            "result": [
                {
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
                    "block_height": str
                },
            ]
        }

        # connect to websocket
        client = DemexWebsocket(f"ws://{DEVEL_AND_CO_SENTRY}:5000/ws")
        # little work around to save the response
        self.response: Optional[dict] = None

        async def on_connect():
            await client.get_recent_trades("recent_trades", "swth_eth1")

        async def on_message(message: dict):
            # save response into self
            self.response = message
            await client.disconnect()

        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait_for(client.connect(on_connect_callback=on_connect,
                                                                    on_receive_message_callback=on_message),
                                                     WEBSOCKET_TIMEOUT_GET_REQUEST))
        except concurrent.futures._base.TimeoutError:
            raise TimeoutError("Test did not complete in time.")

        if not self.response:
            raise RuntimeError("Did not receive a response.")

        self.assertDictStructure(expect, self.response)

        # TODO remove or change if id in trade is no longer 'id'
        for trade in self.response["result"]:
            self.assertTrue(trade["id"] == "0", msg="Expected id to be '0'")
