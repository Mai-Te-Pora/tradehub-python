import random
from tradehub.authenticated_client import AuthenticatedClient
from tests import APITestCase, TESTNET_VAL_IP, TRADING_TESTNET_WALLET_MNEMONIC
import tradehub.types as types
from tradehub.wallet import Wallet


class TestAuthenticatedClient(APITestCase):

    def setUp(self) -> None:
        self.validator_addresses = ['tswthvaloper1hn0spc9plh5ker8lrtzyz9uqfe3xk2yn0c6nyf', 'tswthvaloper10229tj7kh2mzwsn9cnfxuq3sqjuph860dlezpr']
        self.validator_address = self.validator_addresses[random.randint(a=0, b=len(self.validator_addresses)-1)]
        self.validator_dst_address = self.validator_addresses
        self.validator_dst_address.remove(self.validator_address)
        self.validator_dst_address = self.validator_dst_address[0]
        self._wallet: Wallet = Wallet(mnemonic=TRADING_TESTNET_WALLET_MNEMONIC, network="testnet")
        self.authenticated_client: AuthenticatedClient = AuthenticatedClient(wallet=self._wallet,
                                                                             node_ip=TESTNET_VAL_IP,
                                                                             node_port=5001,
                                                                             network="testnet")
        self.expect: dict = {
            'height': str,
            'txhash': str,
            'raw_log': str,
            'logs': [{
                'msg_index': int,
                'log': str,
                'events': [{
                    'type': str,
                    'attributes': [{
                        'key': str,
                        'value': str
                    }]
                }]
            }],
            'gas_wanted': str,
            'gas_used': str
        }

    def test_update_profile(self):
        txn_message: dict = types.UpdateProfileMessage(username='PythonCICD', twitter='PythonCICD')
        result: dict = self.authenticated_client.update_profile(message=txn_message)

        self.assertDictStructure(expect=self.expect, actual=result)

    def test_send_tokens(self):
        txn_message: dict = types.SendTokensMessage(to_address='tswth1rjr3nm2xcyr6psseksk8vhpc4n33htntuhmdfm',
                                                    amount=[types.SendTokensAmount(amount='5.1', denom='swth')])
        result: dict = self.authenticated_client.send_tokens(message=txn_message)

        self.assertDictStructure(expect=self.expect, actual=result)

    def test_create_order(self):
        txn_message: dict = types.CreateOrderMessage(market='swth_eth',
                                                     side="sell",
                                                     quantity="200",
                                                     type="market")
        result: dict = self.authenticated_client.create_order(message=txn_message)

        self.assertDictStructure(expect=self.expect, actual=result)

    def test_stake_switcheo(self):
        txn_message: dict = types.DelegateTokensMessage(delegator_address=self._wallet.address,
                                                        validator_address=self.validator_address,
                                                        amount=types.DelegateTokensAmount(amount='5.1', denom='swth'))
        result: dict = self.authenticated_client.stake_switcheo(message=txn_message)

        self.assertDictStructure(expect=self.expect, actual=result)

    def test_claim_staking_rewards(self):
        txn_message: dict = types.WithdrawDelegatorRewardsMessage(delegator_address=self._wallet.address,
                                                                  validator_address='tswthvaloper10229tj7kh2mzwsn9cnfxuq3sqjuph860dlezpr')
        result: dict = self.authenticated_client.claim_staking_rewards(message=txn_message)

        self.assertDictStructure(expect=self.expect, actual=result)

    def test_claim_all_staking_rewards(self):
        validator_addresses = []
        delegation_rewards: dict = self.authenticated_client.get_delegation_rewards(swth_address=self._wallet.address)
        for delegation_reward in delegation_rewards["result"]["rewards"]:
            validator_addresses.append(delegation_reward["validator_address"])

        txn_message: dict = types.WithdrawAllDelegatorRewardsParams(delegator_address=self._wallet.address,
                                                                    validator_addresses=validator_addresses)
        result: dict = self.authenticated_client.claim_all_staking_rewards(message=txn_message)

        self.assertDictStructure(expect=self.expect, actual=result)

    def test_unbond_tokens(self):
        expect: dict = self.expect
        expect['data'] = str
        txn_message: dict = types.BeginUnbondingTokensMessage(delegator_address=self._wallet.address,
                                                              validator_address=self.validator_address,
                                                              amount=types.AmountMessage(amount='1.1', denom='swth'))
        result: dict = self.authenticated_client.unbond_tokens(message=txn_message)

        self.assertDictStructure(expect=expect, actual=result)

    def test_redelegate_tokens(self):
        expect: dict = self.expect
        expect['data'] = str
        txn_message: dict = types.BeginRedelegatingTokensMessage(delegator_address=self._wallet.address,
                                                                 validator_src_address=self.validator_address,
                                                                 validator_dst_address=self.validator_dst_address,
                                                                 amount=types.AmountMessage(amount='1.1', denom='swth'))
        result: dict = self.authenticated_client.redelegate_tokens(message=txn_message)

        self.assertDictStructure(expect=expect, actual=result)
