import asyncio
import concurrent
from typing import Optional, List

from tests import APITestCase, DEVEL_AND_CO_SENTRY, WALLET_SWTH_ETH1_AMM, WEBSOCKET_TIMEOUT_SUBSCRIPTION
from tradehub.websocket_client import DemexWebsocket


class TestWSSubscribeAccountTrades(APITestCase):

    def test_subscribe_account_trades_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """
        expect_subscription: dict = {
            'id': str,
            'result': [str]
        }

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
        self.response: List[dict] = []

        async def on_connect():
            # use AMM to be sure deterministic of which tokens the wallet holds
            await client.subscribe_account_trades('balance', WALLET_SWTH_ETH1_AMM)

        async def on_message(message: dict):
            # save response into self
            self.response.append(message)

        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait_for(client.connect(on_connect_callback=on_connect,
                                                                    on_receive_message_callback=on_message),
                                                     WEBSOCKET_TIMEOUT_SUBSCRIPTION))
        except concurrent.futures._base.TimeoutError:
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


    def test_subscribe_account_market_trades_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """
        expect_subscription: dict = {
            'id': str,
            'result': [str]
        }

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
        self.response: List[dict] = []

        async def on_connect():
            # use AMM to be sure deterministic of which tokens the wallet holds
            await client.subscribe_account_trades('balance', WALLET_SWTH_ETH1_AMM, "swth_eth1")

        async def on_message(message: dict):
            # save response into self
            self.response.append(message)

        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait_for(client.connect(on_connect_callback=on_connect,
                                                                    on_receive_message_callback=on_message),
                                                     WEBSOCKET_TIMEOUT_SUBSCRIPTION))
        except concurrent.futures._base.TimeoutError:
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


