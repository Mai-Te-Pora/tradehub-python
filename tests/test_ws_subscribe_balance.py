import asyncio
import concurrent
from typing import Optional, List

from tests import APITestCase, DEVEL_AND_CO_SENTRY, WALLET_SWTH_ETH1_AMM, WEBSOCKET_TIMEOUT_SUBSCRIPTION
from tradehub.websocket_client import DemexWebsocket


class TestWSSubscribeBalance(APITestCase):

    def test_subscribe_balance_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """
        expect_subscription: dict = {
            'id': str,
            'result': [str]
        }

        balance: dict = {
            'available': str,
            'order': str,
            'position': str,
            'denom': str
        }

        expect: dict = {
            'channel': str,
            'result': {
                'eth1': balance,
                'eth1-80-swth-20-lp1': balance,
                'swth': balance
            }
        }

        # connect to websocket
        client = DemexWebsocket(f"ws://{DEVEL_AND_CO_SENTRY}:5000/ws")
        # little work around to save the response
        self.response: List[dict] = []

        async def on_connect():
            # use AMM to be sure deterministic of which tokens the wallet holds
            await client.subscribe_balances('balance', WALLET_SWTH_ETH1_AMM)

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

        self.assertTrue(len(self.response) >= 2, msg=f"Expected at least 2 messages: channel subscription and and first update message")

        channel_subscription: dict = self.response[0]
        self.assertDictStructure(expect_subscription, channel_subscription)

        for message in self.response[1:]:
            # if this fails, check if the AMM wallet own other tokens as expected
            self.assertDictStructure(expect, message)

