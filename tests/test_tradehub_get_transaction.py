from tests import APITestCase, DEVEL_AND_CO_SENTRY
from tradehub.public_client import PublicClient


class TestTradeHubGetTransaction(APITestCase):

    def setUp(self) -> None:
        self._client = PublicClient(DEVEL_AND_CO_SENTRY)

    def test_get_transaction_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            "id": str,
            "hash": str,
            "address": str,
            "username": str,
            "msgs": [
                {
                    "msg_type": str,
                    "msg": str
                }
            ],
            "code": str,
            "gas_used": str,
            "gas_limit": str,
            "memo": str,
            "height": str,
            "block_time": str
        }

        result: dict = self._client.get_transaction("A93BEAC075562D4B6031262BDDE8B9A720346A54D8570A881E3671FEB6E6EFD4")

        self.assertDictStructure(expect, result)
