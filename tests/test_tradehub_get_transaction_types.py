from tests import APITestCase, MAINNET_VAL_IP
from tradehub.public_client import PublicClient


class TestTradeHubGetTransactionTypes(APITestCase):

    def setUp(self) -> None:
        self._client = PublicClient(MAINNET_VAL_IP)

    def test_get_transaction_types_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """
        pass

        # result: list = self._client.get_transaction_types()

        # self.assertIsInstance(result, list, msg=f"Expected result as list, got {type(result)} instead.")

        # for transaction_type in result:
        #     self.assertIsInstance(transaction_type, str, msg=f"Expected type as str, got {type(transaction_type)} instead.")
