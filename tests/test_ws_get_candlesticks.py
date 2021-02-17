import asyncio
import concurrent
from typing import Optional

from tests import APITestCase, DEVEL_AND_CO_SENTRY, WEBSOCKET_TIMEOUT_GET_REQUEST
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
        client = DemexWebsocket(f"ws://{DEVEL_AND_CO_SENTRY}:5000/ws")
        # little work around to save the response
        self.response: Optional[dict] = None

        async def on_connect():
            await client.get_candlesticks('candlesticks', "swth_eth1", 5)

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
