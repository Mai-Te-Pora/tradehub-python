import asyncio
from typing import Optional, List

from tests import APITestCase, MAINNET_VAL_IP, WEBSOCKET_TIMEOUT_GET_REQUEST
from tradehub.websocket_client import DemexWebsocket


class TestWSGetCandlesticks(APITestCase):

    def test_get_candlesticks_structure(self):
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
        client = DemexWebsocket(f"ws://{MAINNET_VAL_IP}:5000/ws")
        # little work around to save the response
        self.response: List[Optional[dict]] = []

        async def on_connect():
            for granularity in [1, 5, 15, 30, 60, 360, 1440]:
                await client.get_candlesticks('candlesticks', "swth_eth1", granularity)

        async def on_message(message: dict):
            # save response into self
            self.response.append(message)

        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait_for(client.connect(on_connect_callback=on_connect,
                                                                    on_receive_message_callback=on_message),
                                                     WEBSOCKET_TIMEOUT_GET_REQUEST))
        except asyncio.TimeoutError:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(client.disconnect())

        if not self.response:
            raise RuntimeError("Did not receive a response.")

        for response in self.response:
            self.assertDictStructure(expect, response)

    def test_get_candlesticks_wrong_granularity(self):
        """
        Check if the method catches wrong granularities.
        :return:
        """

        # connect to websocket
        client = DemexWebsocket("")
        for wrong_granularity in [0, 2, 4, 6, 100, 1500]:
            with self.assertRaises(ValueError):
                loop = asyncio.get_event_loop()
                loop.run_until_complete(client.get_candlesticks("candle", "swth_eth1", wrong_granularity))
