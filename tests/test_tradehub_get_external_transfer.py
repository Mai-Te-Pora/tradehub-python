from tests import APITestCase, MAINNET_VAL_IP, WALLET_DEVEL
from tradehub.public_client import PublicClient
from typing import Union


class TestTradeHubGetExternalTransfers(APITestCase):

    def setUp(self) -> None:
        self._client = PublicClient(MAINNET_VAL_IP)

    def test_get_external_transfers(self):
        """
        Check if response match expected dict structure.
        :return:
        """
        # TODO need test wallet to be deterministic
        expect: dict = {
            "address": str,
            "amount": str,
            "block_height": int,
            "blockchain": str,
            "contract_hash": str,
            "denom": str,
            "fee_address": Union[str, None],
            "fee_amount": str,
            "id": str,
            "status": str,
            "symbol": str,
            "timestamp": int,
            "token_name": str,
            "transaction_hash": str,
            "transfer_type": str
        }

        result: list = self._client.get_external_transfers(WALLET_DEVEL)

        # Can not check this atm, cause it can change need test wallet
        # self.assertEqual(1, len(result), msg="Expected count(1) of external transfers are not returned.")

        for transfer in result:
            self.assertDictStructure(expect, transfer)
