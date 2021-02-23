from tests import APITestCase, mainnet_client, WALLET_VALIDATOR


class TestTradeHubGetDelegationRewards(APITestCase):

    def setUp(self) -> None:
        self._client = mainnet_client

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
