import asyncio
from typing import List

from tests import APITestCase, MAINNET_VAL_IP, WALLET_SWTH_ETH1_AMM, WEBSOCKET_TIMEOUT_SUBSCRIPTION
from tradehub.websocket_client import DemexWebsocket


class TestWSSubscribeOrders(APITestCase):

    def test_subscribe_orders_structure(self):
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
            'result': [
                {
                    'order_id': str,
                    'block_height': int,
                    'triggered_block_height': int,
                    'address': str,
                    'market': str,
                    'side': str,
                    'price': str,
                    'quantity': str,
                    'available': str,
                    'filled': str,
                    'order_status': str,
                    'order_type': str,
                    'initiator': str,
                    'time_in_force': str,
                    'stop_price': str,
                    'trigger_type': str,
                    'allocated_margin_denom': str,
                    'allocated_margin_amount': str,
                    'is_liquidation': bool,
                    'is_post_only': bool,
                    'is_reduce_only': bool,
                    'type': str,
                    'block_created_at': str,
                    'username': str,
                    'id': str
                }
            ]
        }

        # connect to websocket
        client = DemexWebsocket(f"ws://{MAINNET_VAL_IP}:5000/ws")
        # little work around to save the response
        self.response: List[dict] = []

        async def on_connect():
            # use AMM to be sure deterministic of which tokens the wallet holds
            await client.subscribe_orders('orders', WALLET_SWTH_ETH1_AMM)

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

        if len(self.response) < 2:
            self.skipTest(f"Did not receive orders within time, test can not finish.")

        channel_subscription: dict = self.response[0]
        self.assertDictStructure(expect_subscription, channel_subscription)

        for message in self.response[1:]:
            # if this fails, check if the AMM wallet own other tokens as expected
            self.assertDictStructure(expect, message)

    def test_subscribe_market_orders_structure(self):
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
            'result': [
                {
                    'order_id': str,
                    'block_height': int,
                    'triggered_block_height': int,
                    'address': str,
                    'market': str,
                    'side': str,
                    'price': str,
                    'quantity': str,
                    'available': str,
                    'filled': str,
                    'order_status': str,
                    'order_type': str,
                    'initiator': str,
                    'time_in_force': str,
                    'stop_price': str,
                    'trigger_type': str,
                    'allocated_margin_denom': str,
                    'allocated_margin_amount': str,
                    'is_liquidation': bool,
                    'is_post_only': bool,
                    'is_reduce_only': bool,
                    'type': str,
                    'block_created_at': str,
                    'username': str,
                    'id': str
                }
            ]
        }

        # connect to websocket
        client = DemexWebsocket(f"ws://{MAINNET_VAL_IP}:5000/ws")
        # little work around to save the response
        self.response: List[dict] = []

        async def on_connect():
            # use AMM to be sure deterministic of which tokens the wallet holds
            await client.subscribe_orders('orders', WALLET_SWTH_ETH1_AMM, "swth_eth1")

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

        if len(self.response) < 2:
            self.skipTest(f"Did not receive orders within time, test can not finish.")

        channel_subscription: dict = self.response[0]
        self.assertDictStructure(expect_subscription, channel_subscription)

        for message in self.response[1:]:
            # if this fails, check if the AMM wallet own other tokens as expected
            self.assertDictStructure(expect, message)
