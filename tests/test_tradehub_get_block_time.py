from tests import APITestCase, mainnet_client


class TestTradeHubGetBlockTime(APITestCase):

    def setUp(self) -> None:
        self._client = mainnet_client

    def test_get_block_time_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: str = "HH:MM:SS.ZZZZZZ"

        result: str = self._client.get_block_time()

        self.assertIsInstance(result, str)

        self.assertAlmostEqual(len(result), len(expect), msg=f"Check if expected length matches actual length failed.", delta=3)
