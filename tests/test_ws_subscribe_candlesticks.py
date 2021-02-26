import asyncio
from typing import List

from tests import APITestCase, MAINNET_WS_URI, WEBSOCKET_TIMEOUT_SUBSCRIPTION
from tradehub.websocket_client import DemexWebsocket


class TestWSSubscribeCandlesticks(APITestCase):

    def test_subscribe_candlesticks_structure(self):
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
            'result': {
                'id': int,
                'market': str,
                'time': str,
                'resolution': int,
                'open': str,
                'close': str,
                'high': str,
                'low': str,
                'volume': str,
                'quote_volume': str,
            }
        }

        # connect to websocket
        client = DemexWebsocket(uri=MAINNET_WS_URI)
        # little work around to save the response
        self.response: List[dict] = []

        async def on_connect():
            await client.subscribe_candlesticks('candlesticks', "swth_eth1", 1)

        async def on_message(message: dict):
            # save response into self
            print(message)
            self.response.append(message)

        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait_for(client.connect(on_connect_callback=on_connect,
                                                                    on_receive_message_callback=on_message),
                                                     2*WEBSOCKET_TIMEOUT_SUBSCRIPTION))
        except asyncio.TimeoutError:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(client.disconnect())

        if not self.response:
            raise RuntimeError("Did not receive a response.")

        if len(self.response) < 2:
            self.skipTest(f"Did not receive candlesticks within time, test can not finish.")

        channel_subscription: dict = self.response[0]
        self.assertDictStructure(expect_subscription, channel_subscription)

        for message in self.response[1:]:
            if message["result"]:
                self.assertDictStructure(expect, message)

    def test_subscribe_candlesticks_wrong_granularity(self):
        """
        Check if the method catches wrong granularities.
        :return:
        """

        # connect to websocket
        client = DemexWebsocket("")
        for wrong_granularity in [0, 2, 4, 6, 100, 1500]:
            with self.assertRaises(ValueError):
                loop = asyncio.get_event_loop()
                loop.run_until_complete(client.subscribe_candlesticks("candle", "swth_eth1", wrong_granularity))
