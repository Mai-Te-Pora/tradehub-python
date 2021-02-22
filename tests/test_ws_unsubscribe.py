from typing import List

from tests import APITestCase, MAINNET_VAL_IP, WALLET_SWTH_ETH1_AMM, WEBSOCKET_TIMEOUT_GET_REQUEST
from tradehub.websocket_client import DemexWebsocket


class TestWSUnsubscribe(APITestCase):

    def test_unsubscribe_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """
        expect_subscription: dict = {
            'id': str,
            'result': [str]
        }

        # connect to websocket
        client = DemexWebsocket(f"ws://{MAINNET_VAL_IP}:5000/ws")
        # little work around to save the response
        self.response: List[dict] = []

        async def on_connect():
            # use AMM to be sure deterministic of which tokens the wallet holds
            await client.subscribe_balances('balance', WALLET_SWTH_ETH1_AMM)

        async def on_message(message: dict):
            # save response into self
            if "id" in message.keys():
                self.response.append(message)
            if len(self.response) == 1:
                await client.unsubscribe("unsubscribe", self.response[0]["result"])

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

        self.assertTrue(len(self.response) >= 2, msg=f"Expected at least 2 messages: channel subscription and and first update message")

        channel_subscription: dict = self.response[0]
        self.assertDictStructure(expect_subscription, channel_subscription)
        channel_unsubscription: dict = self.response[1]
        self.assertDictStructure(expect_subscription, channel_unsubscription)
