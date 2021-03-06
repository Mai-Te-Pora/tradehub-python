from tests import APITestCase, mainnet_client


class TestTradeHubGetPrices(APITestCase):

    def setUp(self) -> None:
        self._client = mainnet_client

    def test_get_prices_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            "last": str,
            "index": str,
            "fair": str,
            "mark": str,
            "mark_avg": str,
            "settlement": str,
            "fair_index_delta_avg": str,
            "market": str,
            "marking_strategy": str,
            "index_updated_at": str,
            "last_updated_at": str,
            "block_height": int
        }

        result: dict = self._client.get_prices("swth_eth1")

        self.assertDictStructure(expect, result)

        # Currently the field market is empty, check if this changed
        self.assertTrue(len(result["market"]) == 0, msg="Expected field 'market' to be empty")

    def test_get_prices_empty_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            "last": str,
            "index": str,
            "fair": str,
            "mark": str,
            "mark_avg": str,
            "settlement": str,
            "fair_index_delta_avg": str,
            "market": str,
            "marking_strategy": str,
            "index_updated_at": str,
            "last_updated_at": str,
            "block_height": int
        }

        result: dict = self._client.get_prices("swth_eth1")

        self.assertDictStructure(expect, result)

        # Currently the field market is empty, check if this changed
        self.assertTrue(len(result["market"]) == 0, msg="Expected field 'market' to be empty")
