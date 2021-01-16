from tests import APITestCase, DEVEL_AND_CO_SENTRY
from tradehub.public_client import PublicClient


class TestTradeHubGetBalance(APITestCase):

    def setUp(self) -> None:
        self._client = PublicClient(DEVEL_AND_CO_SENTRY)

    def test_get_balance_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """
        expect: dict = {
            "cel1": {
                "available": str,
                "order": str,
                "position": str,
                "denom": str
            },
            "eth1": {
                "available": str,
                "order": str,
                "position": str,
                "denom": str
            },
            "nex1": {
                "available": str,
                "order": str,
                "position": str,
                "denom": str
            },
            "nneo2": {
                "available": str,
                "order": str,
                "position": str,
                "denom": str
            },
            "swth": {
                "available": str,
                "order": str,
                "position": str,
                "denom": str
            },
            "usdc1":{
                "available": str,
                "order": str,
                "position": str,
                "denom": str
            },
            "wbtc1": {
                "available": str,
                "order": str,
                "position": str,
                "denom": str
            }
        }

        result: dict = self._client.get_balance("swth1vwges9p847l9csj8ehrlgzajhmt4fcq4sd7gzl")
        # if this may fail, check if all denoms are returned. Non zero balances are not returned
        self.assertDictStructure(expect, result)
