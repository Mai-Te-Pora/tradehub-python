from tests import APITestCase, DEVEL_AND_CO_SENTRY
from tradehub.public_client import PublicClient


class TestTradeHubGetAllValidators(APITestCase):

    def setUp(self) -> None:
        self._client = PublicClient(DEVEL_AND_CO_SENTRY)

    def test_get_all_validators_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """
        expect: dict = {
            "OperatorAddress": str,
            "ConsPubKey": str,
            "Jailed": bool,
            "Status": int,
            "Tokens": str,
            "DelegatorShares": str,
            "Description": {
                "moniker": str,
                "identity": str,
                "website": str,
                "security_contact": str,
                "details": str
            },
            "UnbondingHeight": int,
            "UnbondingCompletionTime": str,
            "Commission": {
                "commission_rates": {
                    "rate": str,
                    "max_rate": str,
                    "max_change_rate": str
                },
                "update_time": str
            },
            "MinSelfDelegation": str,
            "ConsAddress": str,
            "ConsAddressByte": str,
            "WalletAddress": str,
            "BondStatus": str
        }

        result: list = self._client.get_all_validators()

        for item in result:
            self.assertDictStructure(expect, item)