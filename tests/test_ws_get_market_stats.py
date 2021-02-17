import asyncio
import concurrent
from typing import Optional

from tests import APITestCase, DEVEL_AND_CO_SENTRY, WEBSOCKET_TIMEOUT_GET_REQUEST, WALLET_DEVEL
from tradehub.websocket_client import DemexWebsocket


class TestWSGetMarketStats(APITestCase):

    def test_get_market_stats_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        market_stats: dict = {
            "day_high": str,
            "day_low": str,
            "day_open": str,
            "day_close": str,
            "day_volume": str,
            "day_quote_volume": str,
            "index_price": str,
            "mark_price": str,
            "last_price": str,
            "market": str,
            "market_type": str,
            "open_interest": str
        }

        expect: dict = {
            'id': str,
            'result': {
                'cel1_usdc1': market_stats,
                'eth1_usdc1': market_stats,
                'eth1_wbtc1': market_stats,
                'nex1_usdc1': market_stats,
                'nneo2_usdc1': market_stats,
                'swth_eth1': market_stats,
                'swth_usdc1': market_stats,
                'wbtc1_usdc1': market_stats

            }
        }

        # connect to websocket
        client = DemexWebsocket(f"ws://{DEVEL_AND_CO_SENTRY}:5000/ws")
        # little work around to save the response
        self.response: Optional[dict] = None

        async def on_connect():
            await client.get_market_stats("market_stats")

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

    def test_get_market_stats_with_param(self):
        """
        Check if response match expected dict structure.
        :return:
        """
        market_stats: dict = {
            "day_high": str,
            "day_low": str,
            "day_open": str,
            "day_close": str,
            "day_volume": str,
            "day_quote_volume": str,
            "index_price": str,
            "mark_price": str,
            "last_price": str,
            "market": str,
            "market_type": str,
            "open_interest": str
        }

        expect: dict = {
            'id': str,
            'result': {
                'cel1_usdc1': market_stats,
                'eth1_usdc1': market_stats,
                'eth1_wbtc1': market_stats,
                'nex1_usdc1': market_stats,
                'nneo2_usdc1': market_stats,
                'swth_eth1': market_stats,
                'swth_usdc1': market_stats,
                'wbtc1_usdc1': market_stats

            }
        }

        # connect to websocket
        client = DemexWebsocket(f"ws://{DEVEL_AND_CO_SENTRY}:5000/ws")
        # little work around to save the response
        self.response: Optional[dict] = None

        async def on_connect():
            await client.get_market_stats("market_stats", "swth_eth1")

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

        # TODO if this test fails, the bug with the not processed parameter is fixed
        self.assertDictStructure(expect, self.response)
