import asyncio
import concurrent
from typing import Optional

from tests import APITestCase, MAINNET_WS_URI, WEBSOCKET_TIMEOUT_GET_REQUEST, WALLET_DEVEL
from tradehub.websocket_client import DemexWebsocket


class TestWSGetAccountTrades(APITestCase):

    def test_get_account_trades_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            "id": str,
            "result": [
                {
                    "base_precision": int,
                    "quote_precision": int,
                    "fee_precision": int,
                    "order_id": str,
                    "market": str,
                    "side": str,
                    "quantity": str,
                    "price": str,
                    "fee_amount": str,
                    "fee_denom": str,
                    "address": str,
                    "block_height": str,
                    "block_created_at": str,
                    "id": int
                }
            ]
        }

        # connect to websocket
        client = DemexWebsocket(uri=MAINNET_WS_URI)
        # little work around to save the response
        self.response: Optional[dict] = None

        async def on_connect():
            await client.get_account_trades('account_trades', WALLET_DEVEL)

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

        self.assertTrue(len(self.response["result"]) == 100, msg=f"Expected 100 recent trades, got {len(self.response['result'])}")

    def test_get_account_trades_pagination(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        # TODO This endpoint does not work currently
        expect: dict = {
            'id': str,
            'error': {
                'code': str,
                'message': str
            }
        }

        # connect to websocket
        client = DemexWebsocket(uri=MAINNET_WS_URI)
        # little work around to save the response
        self.response: Optional[dict] = None

        async def on_connect():
            await client.get_account_trades('account_trades', WALLET_DEVEL, page=1)

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
