import asyncio
from typing import List

from tests import APITestCase, MAINNET_VAL_IP, WEBSOCKET_TIMEOUT_GET_REQUEST
from tradehub.websocket_client import DemexWebsocket


class TestWSSubscribeMarketStats(APITestCase):

    def test_subscribe_market_stats_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """
        expect_subscription: dict = {
            'id': str,
            'result': [str]
        }

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
            'channel': str,
            'sequence_number': int,
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
        client = DemexWebsocket(f"ws://{MAINNET_VAL_IP}:5000/ws")
        # little work around to save the response
        self.response: List[dict] = []

        async def on_connect():
            await client.subscribe_market_stats('market_stats')

        async def on_message(message: dict):
            # save response into self
            print(message)
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

        if len(self.response) < 2:
            self.skipTest(f"{Did not receive candlesticks within time, test can not finish.}")

        print(self.response[1]["result"].keys())

        channel_subscription: dict = self.response[0]
        self.assertDictStructure(expect_subscription, channel_subscription)

        for message in self.response[1:]:
            self.assertDictStructure(expect, message)
