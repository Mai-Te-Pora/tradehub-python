"""
Description:

    Authenticated Client Class for interacting with the Tradehub network.
    This client performs the actions on the tradehub network by submitting transaction on-chain.
    This class is designed to use public nodes for the API and WS clients to use.

Usage::

    from tradehub.authenticated_client import AuthenticatedClient
"""

from tradehub.transactions import Transactions as TradehubTransactions
import tradehub.types as types
from tradehub.utils import to_tradehub_asset_amount, format_withdraw_address
from tradehub.wallet import Wallet


class AuthenticatedClient(TradehubTransactions):
    """
    This class uses a private key to interact with the Tradehub network of validators.

    Execution of this function is as follows::

        AuthenticatedClient(network='mainnet',
                            wallet=Wallet(mnemonic='', network='mainnet')
                            trusted_ips=None,
                            trusted_uris=None)
    """

    '''
    TODO
    # AMM reward % -> /get_amm_reward_percentage
    # Vault types -> /get_vault_types
    # Vaults by address -> /get_vaults?address=${address}
    '''

    def __init__(self, wallet: Wallet, trusted_ips: list = None, trusted_uris: list = None, network: str = "testnet"):
        """
        :param wallet: Wallet Client that contains the attributes necessary for submitting on-chain transactions.
        :type wallet: Wallet
        :param network: The network you want to interact with. Accepts "testnet" or "mainnet".
        :type network: str
        :param trusted_ips: Known and trusted IPs to connect to for your API requests.
        :type trusted_ips: list
        :param trusted_uris: Known and trusted URIs to connect to for your API requests.
        :type trusted_uris: list
        """
        TradehubTransactions.__init__(self, wallet=wallet, trusted_ips=trusted_ips, trusted_uris=trusted_uris, network=network)
        self.wallet = wallet

    # Authenticated Client Functions
    '''
        The way each of these functions work follow a similar pattern.
        (1) The function is passed a message that matches a class from the type file.
        (2) That message and matching transaction type are sent to a function that standardizes builds of transaction sent to the blockchain.
        (3) Inside that standardization are the:
            (3a) - Determination of fees
            (3b) - Transformation of the message class to a Python dictionary/JSON object to facilitate signing and broadcast to the network.
            (3c) - Determination of account details
        (4) With everything standardized, each of the objects are then sent off to be signed and broadcast to the Tradehub blockchain.
    '''
    def update_profile(self, message: types.UpdateProfileMessage, fee: dict = None):
        """
        Function that makes the network requests to the Tradehub validators across the network.

        Execution of this function is as follows::

            update_profile(message=types.UpdateProfileMessage(username='PythonCICD', twitter='PythonCICD'))

        The expected return result for this function is as follows::

            {
                'height': '1927295',
                'txhash': 'C6AF947EE35EE5282BD140F9F51614FA1C7ACADAB263B921621097C786C06977',
                'raw_log': ...,
                'logs': ...,
                'gas_wanted': '100000000000',
                'gas_used': '68345'
            }

        :param message: UpdateProfileMessage Type that is a class of attributes required to make this on-chain action.
        :param fee: Dict of the fee type, generally this can be left blank and allow the API to handle this.
        :return: Dictionary of the transaction response sent on-chain.
        """
        transaction_type = "UPDATE_PROFILE_MSG_TYPE"
        return self.submit_transaction_on_chain(messages=[message], transaction_type=transaction_type, fee=fee)

    def send_tokens(self, message: types.SendTokensMessage, fee: dict = None):
        """
        Function to send tokens from your wallet to a recipient.

        Execution of this function is as follows::

            sent_tokens(message=types.SendTokensMessage(to_address=send_address,
                                                        amount=types.SendTokensAmount(amount='10.1', denom='swth')))

        :param message: SendTokensMessage Type that is a class of attributes required to make this on-chain action.
        :param fee: Dict of the fee type, generally this can be left blank and allow the API to handle this.
        :return: Dictionary of the transaction response sent on-chain, look in the logs to be sure it matches what was sent.
        """
        transaction_type = "SEND_TOKENS_TYPE"
        if hasattr(message, 'from_address') and message.from_address in [None, ""]:
            message.from_address = self.wallet.address
        amounts = []
        for amount in message.amount:
            formatted_amount = to_tradehub_asset_amount(amount=float(amount.amount), decimals=self.tokens[amount.denom]["decimals"])
            amounts.append(types.SendTokensAmount(amount=formatted_amount, denom=amount.denom))
        message.amount = sorted(amounts, key=lambda x: x.denom.lower())  # When dealing with coin lists in Cosmos it is a requirement that they be ordered by name - https://github.com/cosmos/cosmos-sdk/blob/master/types/coin.go#L215
        return self.submit_transaction_on_chain(messages=[message], transaction_type=transaction_type, fee=fee)

    def create_order(self, message: types.CreateOrderMessage, fee: dict = None):
        """
        Function to create an order on the Tradehub network.

        Execution of this function is as follows::

            create_order(message=types.CreateOrderMessage(market="swth_eth1",
                                                          side="sell",
                                                          quantity="200",
                                                          price="0.00002",
                                                          type="limit"))

        :param message: CreateOrderMessage Type that is a class of attributes required to make this on-chain action.
        :param fee: Dict of the fee type, generally this can be left blank and allow the API to handle this.
        :return: Dictionary of the transaction response sent on-chain, look in the logs to be sure it matches what was sent.
        """
        return self.create_orders(messages=[message], fee=fee)

    def create_orders(self, messages: [types.CreateOrderMessage], fee: dict = None):
        """
        Function to create multiple orders on the Tradehub network.

        Execution of this function is as follows::

            create_orders([message=types.CreateOrderMessage(market="swth_eth1",
                                                            side="sell",
                                                            quantity="200",
                                                            price="0.00002",
                                                            type="limit")])

        :param message: List of CreateOrderMessage Type that is a class of attributes required to make this on-chain action.
        :param fee: Dict of the fee type, generally this can be left blank and allow the API to handle this.
        :return: Dictionary of the transaction response sent on-chain, look in the logs to be sure it matches what was sent.
        """
        transaction_type = "CREATE_ORDER_MSG_TYPE"
        return self.submit_transaction_on_chain(messages=messages, transaction_type=transaction_type, fee=fee)

    def cancel_order(self, message: types.CancelOrderMessage, fee: dict = None):
        """
        Function to cancel an order on the Tradehub network.

        Execution of this function is as follows::

            cancel_order(message=types.CancelOrderMessage(id="D3F370A91D260DB3B1112757D8F9B66EEA1B7887FB4B247872D367F04A4C56EB"))

        :param message: CancelOrderMessage Type that is a class of attributes required to make this on-chain action.
        :param fee: Dict of the fee type, generally this can be left blank and allow the API to handle this.
        :return: Dictionary of the transaction response sent on-chain, look in the logs to be sure it matches what was sent.
        """
        return self.cancel_orders(messages=[message], fee=fee)

    def cancel_orders(self, messages: [types.CancelOrderMessage], fee: dict = None):
        """
        Function to cancel multiple order on the Tradehub network.

        Execution of this function is as follows::

            cancel_orders(message=[types.CancelOrderMessage(id="D3F370A91D260DB3B1112757D8F9B66EEA1B7887FB4B247872D367F04A4C56EB")])

        :param message: List of CancelOrderMessage Type that is a class of attributes required to make this on-chain action.
        :param fee: Dict of the fee type, generally this can be left blank and allow the API to handle this.
        :return: Dictionary of the transaction response sent on-chain, look in the logs to be sure it matches what was sent.
        """
        transaction_type = "CANCEL_ORDER_MSG_TYPE"
        return self.submit_transaction_on_chain(messages=messages, transaction_type=transaction_type, fee=fee)

    def cancel_all(self, message: types.CancelAllMessage, fee: dict = None):
        """
        Function to cancel all orders for a specific market on the Tradehub network.

        Execution of this function is as follows::

            cancel_all(message=types.CancelAllMessage(market='swth_eth1'))

        :param message: CancelAllMessage Type that is a class of attributes required to make this on-chain action.
        :param fee: Dict of the fee type, generally this can be left blank and allow the API to handle this.
        :return: Dictionary of the transaction response sent on-chain, look in the logs to be sure it matches what was sent.
        """
        transaction_type = "CANCEL_ALL_MSG_TYPE"
        return self.submit_transaction_on_chain(messages=[message], transaction_type=transaction_type, fee=fee)

    def edit_order(self, message: types.EditOrderMessage, fee: dict = None):
        """
        Function to edit an open order on the Tradehub network.

        Execution of this function is as follows::

            edit_order(message=types.EditOrderMessage(id="816F6D321F696EA81EB9961BE51DB5CB31520217DAF75FA569446BDD85A21E96",
                                                      quantity="220",
                                                      stop_price="0.0000175"))


        :param message: EditOrderMessage Type that is a class of attributes required to make this on-chain action.
        :param fee: Dict of the fee type, generally this can be left blank and allow the API to handle this.
        :return: Dictionary of the transaction response sent on-chain, look in the logs to be sure it matches what was sent.
        """
        return self.edit_orders(messages=[message], fee=fee)

    def edit_orders(self, messages: [types.EditOrderMessage], fee: dict = None):
        """
        Function to edit open orders on the Tradehub network.

        Execution of this function is as follows::

            edit_orders(message=[types.EditOrderMessage(id="816F6D321F696EA81EB9961BE51DB5CB31520217DAF75FA569446BDD85A21E96",
                                                        quantity="220",
                                                        stop_price="0.0000175")])

        :param message: List of EditOrderMessage Type that is a class of attributes required to make this on-chain action.
        :param fee: Dict of the fee type, generally this can be left blank and allow the API to handle this.
        :return: Dictionary of the transaction response sent on-chain, look in the logs to be sure it matches what was sent.
        """
        transaction_type = "EDIT_ORDER_MSG_TYPE"
        return self.submit_transaction_on_chain(messages=messages, transaction_type=transaction_type, fee=fee)

    # def set_leverage(self, message: types.SetLeverageMessage, fee: dict = None):
    #     return self.set_leverages(messages=[message], fee=fee)

    # def set_leverages(self, messages: [types.SetLeverageMessage], fee: dict = None):
    #     transaction_type = "SET_LEVERAGE_MSG_TYPE"
    #     return self.submit_transaction_on_chain(messages=messages, transaction_type=transaction_type, fee=fee)

    # def edit_margin(self, message: types.EditMarginMessage, fee: dict = None):
    #     return self.edit_margins(messages=[message], fee=fee)

    # def edit_margins(self, messages: [types.EditMarginMessage], fee: dict = None):
    #     transaction_type = "EDIT_MARGIN_MSG_TYPE"
    #     return self.submit_transaction_on_chain(messages=messages, transaction_type=transaction_type, fee=fee)

    def stake_switcheo(self, message=types.DelegateTokensMessage, fee: dict = None):
        """
        Function to stake (or delegate) Switcheo to validators on the Tradehub network.

        Execution of this function is as follows::

            stake_switcheo(message=types.DelegateTokensMessage(delegator_address=self._wallet.address,
                                                               validator_address='tswthvaloper1hn0spc9plh5ker8lrtzyz9uqfe3xk2yn0c6nyf',
                                                               amount=types.DelegateTokensAmount(amount = '10.1', denom = 'swth')))

        :param message: DelegateTokensMessage Type that is a class of attributes required to make this on-chain action.
        :param fee: Dict of the fee type, generally this can be left blank and allow the API to handle this.
        :return: Dictionary of the transaction response sent on-chain, look in the logs to be sure it matches what was sent.
        """
        transaction_type = "DELEGATE_TOKENS_MSG_TYPE"
        message.amount.amount = to_tradehub_asset_amount(amount=float(message.amount.amount), decimals=self.tokens["swth"]["decimals"])
        return self.submit_transaction_on_chain(messages=[message], transaction_type=transaction_type, fee=fee)

    def claim_staking_rewards(self, message=types.WithdrawDelegatorRewardsMessage, fee: dict = None):
        """
        Function to claim rewards generated from staking with a Switcheo validator on the Tradehub network.

        Execution of this function is as follows::

            claim_staking_rewards(message=types.WithdrawDelegatorRewardsMessage(delegator_address=self._wallet.address,
                                                                                validator_address='tswthvaloper10229tj7kh2mzwsn9cnfxuq3sqjuph860dlezpr'))

        :param message: WithdrawDelegatorRewardsMessage Type that is a class of attributes required to make this on-chain action.
        :param fee: Dict of the fee type, generally this can be left blank and allow the API to handle this.
        :return: Dictionary of the transaction response sent on-chain, look in the logs to be sure it matches what was sent.
        """
        transaction_type = "WITHDRAW_DELEGATOR_REWARDS_MSG_TYPE"
        return self.submit_transaction_on_chain(messages=[message], transaction_type=transaction_type, fee=fee)

    def claim_all_staking_rewards(self, message=types.WithdrawAllDelegatorRewardsParams, fee: dict = None):
        """
        Function to claim rewards generated from all validators a wallet is staking with on the Tradehub network.

        Execution of this function is as follows::

            claim_all_staking_rewards(message=types.WithdrawAllDelegatorRewardsParams(delegator_address=self._wallet.address,
                                                                                      validator_addresses=['tswthvaloper1hn0spc9plh5ker8lrtzyz9uqfe3xk2yn0c6nyf', 'tswthvaloper10229tj7kh2mzwsn9cnfxuq3sqjuph860dlezpr']))

        :param message: WithdrawAllDelegatorRewardsMessage Type that is a class of attributes required to make this on-chain action.
        :param fee: Dict of the fee type, generally this can be left blank and allow the API to handle this.
        :return: Dictionary of the transaction response sent on-chain, look in the logs to be sure it matches what was sent.
        """
        transaction_type = "WITHDRAW_DELEGATOR_REWARDS_MSG_TYPE"
        messages = []
        for validator_address in message.validator_addresses:
            messages.append(types.WithdrawDelegatorRewardsMessage(delegator_address=message.delegator_address, validator_address=validator_address))
        return self.submit_transaction_on_chain(messages=messages, transaction_type=transaction_type, fee=fee)

    def unbond_tokens(self, message: types.BeginUnbondingTokensMessage, fee: dict = None):
        """
        Function to unbond tokens a validator on the Tradehub network.

        Execution of this function is as follows::

            unbond_tokens(message=types.BeginUnbondingTokensMessage(delegator_address=self._wallet.address,
                                                                    validator_address='tswthvaloper1hn0spc9plh5ker8lrtzyz9uqfe3xk2yn0c6nyf',
                                                                    amount=types.AmountMessage(amount='0.1', denom='swth')))

        :param message: BeginUnbondingTokensMessage Type that is a class of attributes required to make this on-chain action.
        :param fee: Dict of the fee type, generally this can be left blank and allow the API to handle this.
        :return: Dictionary of the transaction response sent on-chain, look in the logs to be sure it matches what was sent.
        """
        transaction_type = "BEGIN_UNBONDING_TOKENS_MSG_TYPE"
        message.amount.amount = to_tradehub_asset_amount(amount=float(message.amount.amount), decimals=self.tokens["swth"]["decimals"])
        return self.submit_transaction_on_chain(messages=[message], transaction_type=transaction_type, fee=fee)

    def redelegate_tokens(self, message: types.BeginRedelegatingTokensMessage, fee: dict = None):
        """
        Function to move tokens from one validator to another on the Tradehub network.

        Execution of this function is as follows::

            redelegate_tokens(message=types.BeginRedelegatingTokensMessage(delegator_address=self._wallet.address,
                                                                           validator_src_address='tswthvaloper1hn0spc9plh5ker8lrtzyz9uqfe3xk2yn0c6nyf',
                                                                           validator_dst_address='tswthvaloper10229tj7kh2mzwsn9cnfxuq3sqjuph860dlezpr',
                                                                           amount=types.AmountMessage(amount='0.1', denom='swth'))

        :param message: BeginRedelegatingTokensMessage Type that is a class of attributes required to make this on-chain action.
        :param fee: Dict of the fee type, generally this can be left blank and allow the API to handle this.
        :return: Dictionary of the transaction response sent on-chain, look in the logs to be sure it matches what was sent.
        """
        transaction_type = "BEGIN_REDELEGATING_TOKENS_MSG_TYPE"
        message.amount.amount = to_tradehub_asset_amount(amount=float(message.amount.amount), decimals=self.tokens["swth"]["decimals"])
        return self.submit_transaction_on_chain(messages=[message], transaction_type=transaction_type, fee=fee)

    def create_withdraw(self, message: types.CreateWithdrawMessage, blockchain: str, fee: dict = None):
        """
        Function to withdraw tokens from the Tradehub network onto the desired blockchain.

        Execution of this function is as follows::

            create_withdraw(message=types.CreateWithdrawMessage(to_address=NEO_ADDRESS,
                                                                denom='swth-n',
                                                                amount='87',
                                                                fee_amount="1"),
                            blockchain='NEO')

        :param message: CreateWithdrawMessage Type that is a class of attributes required to make this on-chain action.
        :param blockchain: String to specify if the withdraw is going to the NEO or Ethereum network.
        :param fee: Dict of the fee type, generally this can be left blank and allow the API to handle this.
        :return: Dictionary of the transaction response sent on-chain, look in the logs to be sure it matches what was sent.
        """
        message.fee_address = 'swth1prv0t8j8tqcdngdmjlt59pwy6dxxmtqgycy2h7'
        message.to_address = format_withdraw_address(address=message.to_address, blockchain=blockchain)
        transaction_type = "CREATE_WITHDRAWAL_TYPE"
        return self.submit_transaction_on_chain(messages=[message], transaction_type=transaction_type, fee=fee)

    def create_validator(self, message: types.CreateValidatorMessage, fee: dict = None):
        transaction_type = "CREATE_VALIDATOR_MSG_TYPE"
        return self.submit_transaction_on_chain(messages=[message], transaction_type=transaction_type, fee=fee)

    def create_sub_account(self, message: types.CreateSubAccountMessage, fee: dict = None):
        transaction_type = "CREATE_SUB_ACCOUNT_MSG_TYPE"
        return self.submit_transaction_on_chain(messages=[message], transaction_type=transaction_type, fee=fee)

    def activate_sub_account(self, message: types.ActivateSubAccountMessage, fee: dict = None):
        transaction_type = "ACTIVATE_SUB_ACCOUNT_MSG_TYPE"
        return self.submit_transaction_on_chain(messages=[message], transaction_type=transaction_type, fee=fee)

    def add_liquidity(self, message: types.AddLiquidityMessage, fee: dict = None):
        transaction_type = "ADD_LIQUIDITY_MSG_TYPE"
        if not hasattr(message, 'min_shares'):
            message.min_shares = '0'
        return self.submit_transaction_on_chain(messages=[message], transaction_type=transaction_type, fee=fee)

    def remove_liquidity(self, message: types.RemoveLiquidityMessage, fee: dict = None):
        transaction_type = "REMOVE_LIQUIDITY_MSG_TYPE"
        return self.submit_transaction_on_chain(messages=[message], transaction_type=transaction_type, fee=fee)

    def stake_pool_token(self, message: types.StakePoolTokenMessage, fee: dict = None):
        transaction_type = "STAKE_POOL_TOKEN_MSG_TYPE"
        return self.submit_transaction_on_chain(messages=[message], transaction_type=transaction_type, fee=fee)

    def unstake_pool_token(self, message: types.UnstakePoolTokenMessage, fee: dict = None):
        transaction_type = "UNSTAKE_POOL_TOKEN_MSG_TYPE"
        return self.submit_transaction_on_chain(messages=[message], transaction_type=transaction_type, fee=fee)

    def claim_pool_rewards(self, message: types.ClaimPoolRewardsMessage, fee: dict = None):
        transaction_type = "CLAIM_POOL_REWARDS_MSG_TYPE"
        return self.submit_transaction_on_chain(messages=[message], transaction_type=transaction_type, fee=fee)
