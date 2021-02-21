import jsons
import tradehub.types as types
from tests import APITestCase, WALLET_ADDRESS, WALLET_VALIDATOR, WALLET_PUBLIC_KEY


class TestTradeHubWallet(APITestCase):

    def test_transaction_types(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'CREATE_ORDER_MSG_TYPE': str,
            'CANCEL_ORDER_MSG_TYPE': str,
            'CANCEL_ALL_MSG_TYPE': str,
            'EDIT_ORDER_MSG_TYPE': str,
            'SET_LEVERAGE_MSG_TYPE': str,
            'EDIT_MARGIN_MSG_TYPE': str,
            'CREATE_WITHDRAWAL_TYPE': str,
            'SEND_TOKENS_TYPE': str,
            'CREATE_VALIDATOR_MSG_TYPE': str,
            'DELEGATE_TOKENS_MSG_TYPE': str,
            'BEGIN_UNBONDING_TOKENS_MSG_TYPE': str,
            'BEGIN_REDELEGATING_TOKENS_MSG_TYPE': str,
            'WITHDRAW_DELEGATOR_REWARDS_MSG_TYPE': str,
            'CREATE_SUB_ACCOUNT_MSG_TYPE': str,
            'ACTIVATE_SUB_ACCOUNT_MSG_TYPE': str,
            'UPDATE_PROFILE_MSG_TYPE': str,
            'ADD_LIQUIDITY_MSG_TYPE': str,
            'REMOVE_LIQUIDITY_MSG_TYPE': str,
            'STAKE_POOL_TOKEN_MSG_TYPE': str,
            'UNSTAKE_POOL_TOKEN_MSG_TYPE': str,
            'CLAIM_POOL_REWARDS_MSG_TYPE': str,
        }

        self.assertDictStructure(expect, types.transaction_types)

    def test_fee_types(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'order/MsgCreateOrder': 'create_order',
            'liquiditypool/ClaimPoolRewards': 'claim_pool_rewards',
            'oracle/MsgCreateOracle': 'create_oracle_vote',
            'liquiditypool/CreatePool': 'create_pool',
            'liquiditypool/StakePoolToken': 'stake_pool_token',
            'liquiditypool/UnstakePoolToken': 'unstake_pool_token',
        }

        # self.assertDictStructure(expect, types.fee_types)
        # self.assertDictEqual(expect, types.fee_types)
        self.assertEqual(expect['order/MsgCreateOrder'], types.fee_types['order/MsgCreateOrder'])
        self.assertEqual(expect['liquiditypool/ClaimPoolRewards'], types.fee_types['liquiditypool/ClaimPoolRewards'])
        self.assertEqual(expect['oracle/MsgCreateOracle'], types.fee_types['oracle/MsgCreateOracle'])
        self.assertEqual(expect['liquiditypool/CreatePool'], types.fee_types['liquiditypool/CreatePool'])
        self.assertEqual(expect['liquiditypool/StakePoolToken'], types.fee_types['liquiditypool/StakePoolToken'])
        self.assertEqual(expect['liquiditypool/UnstakePoolToken'], types.fee_types['liquiditypool/UnstakePoolToken'])

    def test_update_profile_message(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'username': str,
            'twitter': str,
            'originator': str,
        }

        test_type = types.UpdateProfileMessage(username="tradehup-python",
                                               twitter="Mai-Te-Pora",
                                               originator=WALLET_ADDRESS)
        self.assertDictStructure(expect, jsons.dump(test_type))

    def test_send_tokens_amount(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'amount': str,
            'denom': str,
        }

        test_type = types.SendTokensAmount(amount="12345",
                                           denom="swth")
        self.assertDictStructure(expect, jsons.dump(test_type))

    def test_send_tokens_message(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'to_address': str,
            'amount': [types.SendTokensAmount],
            'from_address': str,
        }

        send_amount = types.SendTokensAmount(amount="12345",
                                             denom="swth")
        test_type = types.SendTokensMessage(to_address=WALLET_ADDRESS,
                                            amount=[send_amount],
                                            from_address=WALLET_ADDRESS)
        test_type = jsons.dump(test_type)
        test_type['amount'] = [send_amount]
        self.assertDictStructure(expect, test_type)

    def test_create_order_message(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'market': str,
            'side': str,
            'quantity': str,
            'price': str,
            'type': str,
            'time_in_force': str,
            'stop_price': str,
            'trigger_type': str,
            'is_post_only': bool,
            'is_reduce_only': bool,
            'originator': str,
        }

        test_type = types.CreateOrderMessage(market="swth_eth1",
                                             side="swth",
                                             quantity="1",
                                             price="0.1",
                                             type='limit',
                                             time_in_force="gtc",
                                             stop_price="0.2",
                                             trigger_type="stop-limit",
                                             is_post_only=False,
                                             is_reduce_only=False,
                                             originator=WALLET_ADDRESS)
        self.assertDictStructure(expect, jsons.dump(test_type))

    def test_cancel_order_message(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'id': str,
            'originator': str,
        }

        test_type = types.CancelOrderMessage(id="12345",
                                             originator=WALLET_ADDRESS)
        self.assertDictStructure(expect, jsons.dump(test_type))

    def test_cancel_all_message(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'market': str,
            'originator': str,
        }

        test_type = types.CancelAllMessage(market="swth_eth1",
                                           originator=WALLET_ADDRESS)
        self.assertDictStructure(expect, jsons.dump(test_type))

    def test_create_withdraw_message(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'to_address': str,
            'denom': str,
            'amount': str,
            'fee_amount': str,
            'originator': str,
        }

        test_type = types.CreateWithdrawMessage(to_address=WALLET_ADDRESS,
                                                denom="swth",
                                                amount="10",
                                                fee_amount="1",
                                                originator=WALLET_ADDRESS)
        self.assertDictStructure(expect, jsons.dump(test_type))

    def test_delegate_tokens_amount(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'amount': str,
            'denom': str,
        }

        test_type = types.DelegateTokensAmount(amount="12345",
                                               denom="swth")
        self.assertDictStructure(expect, jsons.dump(test_type))

    def test_delegate_tokens_message(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'delegator_address': str,
            'validator_address': str,
            'amount': types.DelegateTokensAmount,
        }

        send_amount = types.DelegateTokensAmount(amount="12345",
                                                 denom="swth")
        test_type = types.DelegateTokensMessage(delegator_address=WALLET_ADDRESS,
                                                validator_address=WALLET_VALIDATOR,
                                                amount=send_amount)
        test_type = jsons.dump(test_type)
        test_type['amount'] = send_amount
        self.assertDictStructure(expect, test_type)

    def test_edit_order_message(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'id': str,
            'quantity': str,
            'price': str,
            'stop_price': str,
            'originator': str,
        }

        test_type = types.EditOrderMessage(id="12345",
                                           quantity="1",
                                           price="0.1",
                                           stop_price="0.2",
                                           originator=WALLET_ADDRESS)
        self.assertDictStructure(expect, jsons.dump(test_type))

    def test_set_leverage_message(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'market': str,
            'leverage': str,
            'originator': str,
        }

        test_type = types.SetLeverageMessage(market="swth_eth1",
                                             leverage="10",
                                             originator=WALLET_ADDRESS)
        self.assertDictStructure(expect, jsons.dump(test_type))

    def test_edit_margin_message(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'market': str,
            'margin': str,
            'originator': str,
        }

        test_type = types.EditMarginMessage(market="swth_eth1",
                                            margin="100",
                                            originator=WALLET_ADDRESS)
        self.assertDictStructure(expect, jsons.dump(test_type))

    def test_withdraw_delegator_rewards_message(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'delegator_address': str,
            'validator_address': str,
        }

        test_type = types.WithdrawDelegatorRewardsMessage(delegator_address=WALLET_VALIDATOR,
                                                          validator_address=WALLET_ADDRESS)
        self.assertDictStructure(expect, jsons.dump(test_type))

    def test_withdraw_all_delegator_rewards_message(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'delegator_address': str,
            'validator_address': str,
        }

        test_type = types.WithdrawAllDelegatorRewardsParams(delegator_address=WALLET_ADDRESS,
                                                            validator_addresses=[WALLET_VALIDATOR])
        for validator_address in test_type.validator_addresses:
            test_val = {
                'delegator_address': test_type.delegator_address,
                'validator_address': validator_address,
            }
            self.assertDictStructure(expect, test_val)

    def test_validator_description(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'moniker': str,
            'identity': str,
            'website': str,
            'details': str,
        }

        test_type = types.ValidatorDescription(moniker="Poon to the Moon",
                                               identity="Devel & Co",
                                               website="http://maitepora.org/",
                                               details="Python API")
        self.assertDictStructure(expect, jsons.dump(test_type))

    def test_validator_commission(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'rate': str,
            'max_rate': str,
            'max_rate_change': str,
        }

        test_type = types.ValidatorCommission(rate="0.04",
                                              max_rate="0.2",
                                              max_rate_change="0.01")
        self.assertDictStructure(expect, jsons.dump(test_type))

    def test_validator_value(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'amount': str,
            'denom': str,
        }

        test_type = types.ValidatorValue(amount="1",
                                         denom="swth")
        self.assertDictStructure(expect, jsons.dump(test_type))

    def test_create_validator_message(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'description': types.ValidatorDescription,
            'commission': types.ValidatorCommission,
            'min_self_delegation': str,
            'delegator_address': str,
            'validator_address': str,
            'pubkey': str,
            'value': types.ValidatorValue,
        }

        test_desc = types.ValidatorDescription(moniker="Poon to the Moon",
                                               identity="Devel & Co",
                                               website="http://maitepora.org/",
                                               details="Python API")
        test_comm = types.ValidatorCommission(rate="0.04",
                                              max_rate="0.2",
                                              max_rate_change="0.01")
        test_value = types.ValidatorValue(amount="1",
                                          denom="swth")
        test_type = types.CreateValidatorMessage(description=test_desc,
                                                 commission=test_comm,
                                                 min_self_delegation="1000",
                                                 delegator_address=WALLET_ADDRESS,
                                                 validator_address=WALLET_VALIDATOR,
                                                 pubkey=WALLET_PUBLIC_KEY,
                                                 value=test_value)
        test_type = jsons.dump(test_type)
        test_type['description'] = test_desc
        test_type['commission'] = test_comm
        test_type['value'] = test_value
        self.assertDictStructure(expect, test_type)

    def test_create_sub_account_message(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'sub_address': str,
            'originator': str,
        }

        test_type = types.CreateSubAccountMessage(sub_address=WALLET_ADDRESS,
                                                  originator=WALLET_ADDRESS)
        self.assertDictStructure(expect, jsons.dump(test_type))

    def test_activate_sub_account_message(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'expected_main_account': str,
            'originator': str,
        }

        test_type = types.ActivateSubAccountMessage(expected_main_account=WALLET_ADDRESS,
                                                    originator=WALLET_ADDRESS)
        self.assertDictStructure(expect, jsons.dump(test_type))

    def test_amount_message(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'amount': str,
            'denom': str,
        }

        test_type = types.AmountMessage(amount='1',
                                        denom='swth')
        self.assertDictStructure(expect, jsons.dump(test_type))

    def test_begin_unbonding_tokens_message(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'delegator_address': str,
            'validator_address': str,
            'amount': types.AmountMessage,
        }

        test_amount = types.AmountMessage(amount='1',
                                          denom='swth')
        test_type = types.BeginUnbondingTokensMessage(delegator_address=WALLET_ADDRESS,
                                                      validator_address=WALLET_VALIDATOR,
                                                      amount=test_amount)
        test_type = jsons.dump(test_type)
        test_type['amount'] = test_amount
        self.assertDictStructure(expect, test_type)

    def test_begin_redelegating_tokens_message(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'delegator_address': str,
            'validator_src_address': str,
            'validator_dst_address': str,
            'amount': types.AmountMessage,
        }

        test_amount = types.AmountMessage(amount='1',
                                          denom='swth')
        test_type = types.BeginRedelegatingTokensMessage(delegator_address=WALLET_ADDRESS,
                                                         validator_src_address=WALLET_VALIDATOR,
                                                         validator_dst_address=WALLET_VALIDATOR,
                                                         amount=test_amount)
        test_type = jsons.dump(test_type)
        test_type['amount'] = test_amount
        self.assertDictStructure(expect, test_type)

    def test_add_liquidity_message(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'pool_id': str,
            'a_denom': str,
            'a_amount': str,
            'a_max_amount': str,
            'b_denom': str,
            'b_amount': str,
            'b_max_amount': str,
            'originator': str,
        }

        test_type = types.AddLiquidityMessage(pool_id='12345',
                                              a_denom='swth',
                                              a_amount='100',
                                              a_max_amount='100',
                                              b_denom='eth1',
                                              b_amount='10',
                                              b_max_amount='10',
                                              originator=WALLET_ADDRESS)
        self.assertDictStructure(expect, jsons.dump(test_type))

    def test_remove_liquidity_message(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'pool_id': str,
            'shares': str,
            'originator': str,
        }

        test_type = types.RemoveLiquidityMessage(pool_id='12345',
                                                 shares='0.1',
                                                 originator=WALLET_ADDRESS)
        self.assertDictStructure(expect, jsons.dump(test_type))

    def test_stake_pool_token_message(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'denom': str,
            'amount': str,
            'duration': str,
            'originator': str,
        }

        test_type = types.StakePoolTokenMessage(denom='swth',
                                                amount='10',
                                                duration='30',
                                                originator=WALLET_ADDRESS)
        self.assertDictStructure(expect, jsons.dump(test_type))

    def test_unstake_pool_token_message(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'denom': str,
            'amount': str,
            'originator': str,
        }

        test_type = types.UnstakePoolTokenMessage(denom='swth',
                                                  amount='10',
                                                  originator=WALLET_ADDRESS)
        self.assertDictStructure(expect, jsons.dump(test_type))

    def test_claim_pool_rewards_message(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        expect: dict = {
            'pool_id': str,
            'originator': str,
        }

        test_type = types.ClaimPoolRewardsMessage(pool_id='12345',
                                                  originator=WALLET_ADDRESS)
        self.assertDictStructure(expect, jsons.dump(test_type))
