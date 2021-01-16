from tests import APITestCase, DEVEL_AND_CO_SENTRY, WALLET_VALIDATOR
from tradehub.public_client import PublicClient


class TestTradeHubGetDelegationRewards(APITestCase):

    def setUp(self) -> None:
        self._client = PublicClient(DEVEL_AND_CO_SENTRY)

    def test_get_delegation_rewards_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            "height": str,
            "result": {
                "rewards": [
                    {
                        "validator_address": str,
                        "reward": [
                            {
                                "denom": str,
                                "amount": str
                            }
                        ]
                    }
                ],
                "total": [
                    {
                        "denom": str,
                        "amount": str
                    },
                ]
            }
        }

        result: dict = self._client.get_delegation_rewards(WALLET_VALIDATOR)

        self.assertDictStructure(expect, result)