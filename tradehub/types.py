from collections import defaultdict
from dataclasses import dataclass
from typing import List


transaction_types = {}

# // Orders
transaction_types["CREATE_ORDER_MSG_TYPE"] = 'order/MsgCreateOrder'
transaction_types["CANCEL_ORDER_MSG_TYPE"] = 'order/MsgCancelOrder'
transaction_types["CANCEL_ALL_MSG_TYPE"] = 'order/MsgCancelAll'
transaction_types["EDIT_ORDER_MSG_TYPE"] = 'order/MsgEditOrder'
# export const CREATE_MARKET_MSG_TYPE = 'market/MsgCreateMarket'
# export const UPDATE_MARKET_MSG_TYPE = 'market/MsgUpdateMarket'
# export const INITIATE_SETTLEMENT_MSG_TYPE = 'broker/MsgInitiateSettlement'
# export const SET_TRADING_FLAG_MSG_TYPE = 'order/MsgSetTradingFlag'

# // Positions
transaction_types["SET_LEVERAGE_MSG_TYPE"] = 'leverage/MsgSetLeverage'
transaction_types["EDIT_MARGIN_MSG_TYPE"] = 'position/MsgSetMargin'

# // Tokens
# export const MINT_TOKEN_MSG_TYPE = 'coin/MsgMintToken'
# export const CREATE_TOKEN_MSG_TYPE = 'coin/MsgCreateToken'
transaction_types["CREATE_WITHDRAWAL_TYPE"] = 'coin/MsgWithdraw'
transaction_types["SEND_TOKENS_TYPE"] = 'cosmos-sdk/MsgSend'

# // Oracle
# export const CREATE_ORACLE_TYPE = 'oracle/MsgCreateOracle'
# export const CREATE_VOTE_TYPE = 'oracle/MsgCreateVote'

# // Staking
transaction_types["CREATE_VALIDATOR_MSG_TYPE"] = 'cosmos-sdk/MsgCreateValidator'
transaction_types["DELEGATE_TOKENS_MSG_TYPE"] = 'cosmos-sdk/MsgDelegate'
transaction_types["BEGIN_UNBONDING_TOKENS_MSG_TYPE"] = 'cosmos-sdk/MsgUndelegate'
transaction_types["BEGIN_REDELEGATING_TOKENS_MSG_TYPE"] = 'cosmos-sdk/MsgBeginRedelegate'
transaction_types["WITHDRAW_DELEGATOR_REWARDS_MSG_TYPE"] = 'cosmos-sdk/MsgWithdrawDelegationReward'

# // Accounts
transaction_types["CREATE_SUB_ACCOUNT_MSG_TYPE"] = 'subaccount/MsgCreateSubAccountV1'
transaction_types["ACTIVATE_SUB_ACCOUNT_MSG_TYPE"] = 'subaccount/MsgActivateSubAccountV1'

# // Profile
transaction_types["UPDATE_PROFILE_MSG_TYPE"] = 'profile/MsgUpdateProfile'


# // Gov
# export const SUBMIT_PROPOSAL_TYPE = 'cosmos-sdk/MsgSubmitProposal'
# export const DEPOSIT_PROPOSAL_TYPE = 'cosmos-sdk/MsgDeposit'
# export const VOTE_PROPOSAL_TYPE = 'cosmos-sdk/MsgVote'

# // AMM
transaction_types["ADD_LIQUIDITY_MSG_TYPE"] = 'liquiditypool/AddLiquidity'
transaction_types["REMOVE_LIQUIDITY_MSG_TYPE"] = 'liquiditypool/RemoveLiquidity'
# export const CREATE_POOL_MSG_TYPE = 'liquiditypool/CreatePool'
# export const CREATE_POOL_WITH_LIQUIDITY_MSG_TYPE = 'liquiditypool/CreatePoolWithLiquidity'
# export const LINK_POOL_MSG_TYPE = 'liquiditypool/LinkPool'
# export const UNLINK_POOL_MSG_TYPE = 'liquiditypool/UnlinkPool'
# export const SET_REWARDS_WEIGHTS_MSG_TYPE = 'liquiditypool/SetRewardsWeights'
# export const SET_REWARD_CURVE_MSG_TYPE = 'liquiditypool/SetRewardCurve'
# export const SET_COMMITMENT_CURVE_MSG_TYPE = 'liquiditypool/SetCommitmentCurve'
transaction_types["STAKE_POOL_TOKEN_MSG_TYPE"] = 'liquiditypool/StakePoolToken'
transaction_types["UNSTAKE_POOL_TOKEN_MSG_TYPE"] = 'liquiditypool/UnstakePoolToken'
transaction_types["CLAIM_POOL_REWARDS_MSG_TYPE"] = 'liquiditypool/ClaimPoolRewards'
# export const LINK_POOL_PROPOSAL_TYPE = 'liquiditypool/LinkPoolProposal'
# export const SET_REWARD_CURVE_PROPOSAL_TYPE = 'liquiditypool/SetRewardCurveProposal'
# export const SET_REWARDS_WEIGHT_PROPOSAL_TYPE = 'liquiditypool/SetRewardsWeightsProposal'
# export const SET_COMMITMENT_CURVE_PROPOSAL_TYPE = 'liquiditypool/SetCommitmentCurveProposal'
# export const CHANGE_SWAP_FEE_PROPOSAL_TYPE = 'liquiditypool/ChangeSwapFeeProposal'
# export const CHANGE_NUM_QUOTES_PROPOSAL_TYPE = 'liquiditypool/ChangeNumQuotesProposal'

# // CDP
# export const CREATE_VAULT_TYPE_MSG_TYPE = 'collateralizeddebtposition/CreateVaultType'
# export const ADD_COLLATERAL_MSG_TYPE = 'collateralizeddebtposition/AddCollateral'
# export const REMOVE_COLLATERAL_MSG_TYPE = 'collateralizeddebtposition/RemoveCollateral'
# export const ADD_DEBT_MSG_TYPE = 'collateralizeddebtposition/AddDebt'
# export const REMOVE_DEBT_MSG_TYPE = 'collateralizeddebtposition/RemoveDebt'

# // Fee
# export const SET_MESSAGE_FEE_TYPE = 'fee/SetMsgFee'
# export const SET_MESSAGE_FEE_PROPOSAL_TYPE = 'fee/SetMsgFeeProposal'


fee_types = {
    'order/MsgCreateOrder': 'create_order',
    'liquiditypool/ClaimPoolRewards': 'claim_pool_rewards',
    'oracle/MsgCreateOracle': 'create_oracle_vote',
    'liquiditypool/CreatePool': 'create_pool',
    'liquiditypool/StakePoolToken': 'stake_pool_token',
    'liquiditypool/UnstakePoolToken': 'unstake_pool_token',
}

fee_types = defaultdict(lambda: 'default_fee', fee_types)


@dataclass
class UpdateProfileMessage:
    username: str
    twitter: str
    originator: str = None


@dataclass
class SendTokensAmount:
    amount: str
    denom: str


@dataclass
class SendTokensMessage:
    to_address: str
    amount: List[SendTokensAmount]
    from_address: str = None


@dataclass
class CreateOrderMessage:
    market: str
    side: str
    quantity: str
    price: str = None
    type: str = 'limit'               # Order Type
    time_in_force: str = None
    stop_price: str = None
    trigger_type: str = None
    is_post_only: bool = False
    is_reduce_only: bool = False
    originator: str = None


@dataclass
class CancelOrderMessage:
    id: str
    originator: str = None


@dataclass
class CancelAllMessage:
    market: str
    originator: str = None


@dataclass
class CreateWithdrawMessage:
    to_address: str
    denom: str
    amount: str
    fee_amount: str
    originator: str = None


@dataclass
class DelegateTokensAmount:
    amount: str
    denom: str = 'swth'


@dataclass
class DelegateTokensMessage:
    delegator_address: str
    validator_address: str
    amount: DelegateTokensAmount


@dataclass
class EditOrderMessage:
    id: str
    quantity: str = None
    price: str = None
    stop_price: str = None
    originator: str = None


@dataclass
class SetLeverageMessage:
    market: str
    leverage: str
    originator: str = None


@dataclass
class EditMarginMessage:
    market: str
    margin: str
    originator: str = None


@dataclass
class WithdrawDelegatorRewardsMessage:
    delegator_address: str
    validator_address: str


@dataclass
class WithdrawAllDelegatorRewardsParams:
    delegator_address: str
    validator_addresses: [str]


@dataclass
class ValidatorDescription:
    moniker: str
    identity: str
    website: str
    details: str


@dataclass
class ValidatorCommission:
    rate: str
    max_rate: str
    max_rate_change: str


@dataclass
class ValidatorValue:
    amount: str
    denom: str


@dataclass
class CreateValidatorMessage:
    description: ValidatorDescription
    commission: ValidatorCommission
    min_self_delegation: str
    delegator_address: str
    validator_address: str
    pubkey: str
    value: ValidatorValue


@dataclass
class CreateSubAccountMessage:
    sub_address: str
    originator: str = None


@dataclass
class ActivateSubAccountMessage:
    expected_main_account: str
    originator: str = None


@dataclass
class AmountMessage:
    amount: str
    denom: str


@dataclass
class BeginUnbondingTokensMessage:
    delegator_address: str
    validator_address: str
    amount: AmountMessage


@dataclass
class BeginRedelegatingTokensMessage:
    delegator_address: str
    validator_src_address: str
    validator_dst_address: str
    amount: AmountMessage


@dataclass
class AddLiquidityMessage:
    pool_id: str
    a_denom: str = None
    a_amount: str = None
    a_max_amount: str = None
    b_denom: str = None
    b_amount: str = None
    b_max_amount: str = None
    originator: str = None


@dataclass
class RemoveLiquidityMessage:
    pool_id: str
    shares: str
    originator: str = None


@dataclass
class StakePoolTokenMessage:
    denom: str
    amount: str
    duration: str     # in seconds
    originator: str = None


@dataclass
class UnstakePoolTokenMessage:
    denom: str
    amount: str
    originator: str = None


@dataclass
class ClaimPoolRewardsMessage:
    pool_id: str
    originator: str = None
