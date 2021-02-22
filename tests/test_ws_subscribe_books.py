import asyncio
from typing import List

from tests import APITestCase, MAINNET_VAL_IP, WEBSOCKET_TIMEOUT_SUBSCRIPTION
from tradehub.websocket_client import DemexWebsocket


class TestWSSubscribeBooks(APITestCase):

    def test_subscribe_books_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """
        expect_subscription: dict = {
            'id': str,
            'result': [str]
        }

        expect: dict = {
            'channel': str,
            'sequence_number': int,
            'result': [
                {
                    'market': str,
                    'price': str,
                    'quantity': str,
                    'side': str,
                    'type': str
                }
            ]
        }

        # connect to websocket
        client = DemexWebsocket(f"ws://{MAINNET_VAL_IP}:5000/ws")
        # little work around to save the response
        self.response: List[dict] = []

        async def on_connect():
            await client.subscribe_books('book', "eth1_usdc1")

        async def on_message(message: dict):
            # save response into self
            self.response.append(message)

        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait_for(client.connect(on_connect_callback=on_connect,
                                                                    on_receive_message_callback=on_message),
                                                     WEBSOCKET_TIMEOUT_SUBSCRIPTION))
        except asyncio.TimeoutError:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(client.disconnect())

        if not self.response:
            raise RuntimeError("Did not receive a response.")

        self.assertTrue(len(self.response) >= 2, msg=f"Expected at least 2 messages: channel subscription and an update message")

        channel_subscription: dict = self.response[0]
        self.assertDictStructure(expect_subscription, channel_subscription)

        for message in self.response[1:]:
            self.assertDictStructure(expect, message)
