from tradehub.transactions import Transactions as TradehubTransactions
import tradehub.types as types
from tradehub.utils import to_tradehub_asset_amount, format_withdraw_address
from tradehub.wallet import Wallet


class AuthenticatedClient(TradehubTransactions):

    '''
    TODO
    # AMM reward % -> /get_amm_reward_percentage
    # Vault types -> /get_vault_types
    # Vaults by address -> /get_vaults?address=${address}
    '''

    def __init__(self, wallet: Wallet, trusted_ips: list = None, trusted_uris: list = None, network: str = "testnet"):
        """
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
        '''
            message = {
                username: 'PythonAPI',
                twitter: '',
            }
        '''
        transaction_type = "UPDATE_PROFILE_MSG_TYPE"
        return self.submit_transaction_on_chain(messages=[message], transaction_type=transaction_type, fee=fee)

    def send_tokens(self, message: types.SendTokensMessage, fee: dict = None):
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
        '''
            {
                market: "swth_eth",
                side: "sell",
                quantity: "200",
                price: "0.00002",
                order_type: "limit",
            }
        '''
        return self.create_orders(messages=[message], fee=fee)

    def create_orders(self, messages: [types.CreateOrderMessage], fee: dict = None):
        transaction_type = "CREATE_ORDER_MSG_TYPE"
        return self.submit_transaction_on_chain(messages=messages, transaction_type=transaction_type, fee=fee)

    def cancel_order(self, message: types.CancelOrderMessage, fee: dict = None):
        return self.cancel_orders(messages=[message], fee=fee)

    def cancel_orders(self, messages: [types.CancelOrderMessage], fee: dict = None):
        transaction_type = "CANCEL_ORDER_MSG_TYPE"
        return self.submit_transaction_on_chain(messages=messages, transaction_type=transaction_type, fee=fee)

    def cancel_all(self, message: types.CancelAllMessage, fee: dict = None):
        transaction_type = "CANCEL_ALL_MSG_TYPE"
        return self.submit_transaction_on_chain(messages=[message], transaction_type=transaction_type, fee=fee)

    def edit_order(self, message: types.EditOrderMessage, fee: dict = None):
        return self.edit_orders(messages=[message], fee=fee)

    def edit_orders(self, messages: [types.EditOrderMessage], fee: dict = None):
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
        transaction_type = "DELEGATE_TOKENS_MSG_TYPE"
        message.amount.amount = to_tradehub_asset_amount(amount=float(message.amount.amount), decimals=self.tokens["swth"]["decimals"])
        return self.submit_transaction_on_chain(messages=[message], transaction_type=transaction_type, fee=fee)

    def claim_staking_rewards(self, message=types.WithdrawDelegatorRewardsMessage, fee: dict = None):
        transaction_type = "WITHDRAW_DELEGATOR_REWARDS_MSG_TYPE"
        return self.submit_transaction_on_chain(messages=[message], transaction_type=transaction_type, fee=fee)

    def claim_all_staking_rewards(self, message=types.WithdrawAllDelegatorRewardsParams, fee: dict = None):
        transaction_type = "WITHDRAW_DELEGATOR_REWARDS_MSG_TYPE"
        messages = []
        for validator_address in message.validator_addresses:
            messages.append(types.WithdrawDelegatorRewardsMessage(delegator_address=message.delegator_address, validator_address=validator_address))
        return self.submit_transaction_on_chain(messages=messages, transaction_type=transaction_type, fee=fee)

    def unbond_tokens(self, message: types.BeginUnbondingTokensMessage, fee: dict = None):
        transaction_type = "BEGIN_UNBONDING_TOKENS_MSG_TYPE"
        message.amount.amount = to_tradehub_asset_amount(amount=float(message.amount.amount), decimals=self.tokens["swth"]["decimals"])
        return self.submit_transaction_on_chain(messages=[message], transaction_type=transaction_type, fee=fee)

    def redelegate_tokens(self, message: types.BeginRedelegatingTokensMessage, fee: dict = None):
        transaction_type = "BEGIN_REDELEGATING_TOKENS_MSG_TYPE"
        message.amount.amount = to_tradehub_asset_amount(amount=float(message.amount.amount), decimals=self.tokens["swth"]["decimals"])
        return self.submit_transaction_on_chain(messages=[message], transaction_type=transaction_type, fee=fee)

    def create_withdraw(self, message: types.CreateWithdrawMessage, blockchain: str, fee: dict = None):
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
