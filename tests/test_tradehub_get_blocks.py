from tests import APITestCase, MAINNET_VAL_IP
from tradehub.public_client import PublicClient


class TestTradeHubGetBlocks(APITestCase):

    def setUp(self) -> None:
        self._client = PublicClient(MAINNET_VAL_IP)

    def test_get_blocks_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            "block_height": str,
            "time": str,
            "count": str,
            "proposer_address": str
        }

        result: list = self._client.get_blocks()

        self.assertEqual(200, len(result), msg="Expected count(200) off blocks are not returned.")

        for block in result:
            self.assertDictStructure(expect, block)
