from tests import APITestCase, mainnet_client


class TestTradeHubGetOrderbook(APITestCase):

    def setUp(self) -> None:
        self._client = mainnet_client

    def test_get_get_orderbook_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            "asks": [
                {
                    "price": str,
                    "quantity": str
                }
            ],
            "bids": [
                {
                    "price": str,
                    "quantity": str
                }
            ]
        }

        result: dict = self._client.get_orderbook("swth_eth1")

        self.assertDictStructure(expect, result)

    def test_get_orderbook_empty_structure(self):
        expect: dict = {
            "asks": [
            ],
            "bids": [
            ]
        }

        result: dict = self._client.get_orderbook("unknown")
        self.assertDictStructure(expect, result)
