from tests import APITestCase, DEVEL_AND_CO_SENTRY
from tradehub.public_client import PublicClient


class TestTradeHubGetTransactions(APITestCase):

    def setUp(self) -> None:
        self._client = PublicClient(DEVEL_AND_CO_SENTRY)

    def test_get_transactions_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            "id": str,
            "hash": str,
            "address": str,
            "username": str,
            "msg_type": str,
            "msg": str,
            "code": str,
            "gas_used": str,
            "gas_limit": str,
            "memo": str,
            "height": str,
            "block_time": str
        }

        result: list = self._client.get_transactions()

        self.assertEqual(200, len(result), msg="Expected count(200) of transactions are not returned.")

        for transaction in result:
            self.assertDictStructure(expect, transaction)
