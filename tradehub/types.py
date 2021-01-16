from collections import defaultdict
from typing import TypedDict


message_types = {}

# // Orders
message_types["CREATE_ORDER_MSG_TYPE"] = 'order/MsgCreateOrder'
message_types["CANCEL_ORDER_MSG_TYPE"] = 'order/MsgCancelOrder'
message_types["CANCEL_ALL_MSG_TYPE"] = 'order/MsgCancelAll'
message_types["EDIT_ORDER_MSG_TYPE"] = 'order/MsgEditOrder'
# export const CREATE_MARKET_MSG_TYPE = 'market/MsgCreateMarket'
# export const UPDATE_MARKET_MSG_TYPE = 'market/MsgUpdateMarket'
# export const INITIATE_SETTLEMENT_MSG_TYPE = 'broker/MsgInitiateSettlement'
# export const SET_TRADING_FLAG_MSG_TYPE = 'order/MsgSetTradingFlag'

# // Positions
# export const SET_LEVERAGE_MSG_TYPE = 'leverage/MsgSetLeverage'
# export const EDIT_MARGIN_MSG_TYPE = 'position/MsgSetMargin'

# // Tokens
# export const MINT_TOKEN_MSG_TYPE = 'coin/MsgMintToken'
# export const CREATE_TOKEN_MSG_TYPE = 'coin/MsgCreateToken'
# export const CREATE_WITHDRAWAL_TYPE = 'coin/MsgWithdraw'
# export const SEND_TOKENS_TYPE = 'cosmos-sdk/MsgSend'

# // Oracle
# export const CREATE_ORACLE_TYPE = 'oracle/MsgCreateOracle'
# export const CREATE_VOTE_TYPE = 'oracle/MsgCreateVote'

# // Staking
# export const CREATE_VALIDATOR_MSG_TYPE = 'cosmos-sdk/MsgCreateValidator'
# export const DELEGATE_TOKENS_MSG_TYPE = 'cosmos-sdk/MsgDelegate'
# export const BEGIN_UNBONDING_TOKENS_MSG_TYPE = 'cosmos-sdk/MsgUndelegate'
# export const BEGIN_REDELEGATING_TOKENS_MSG_TYPE = 'cosmos-sdk/MsgBeginRedelegate'
message_types["WITHDRAW_DELEGATOR_REWARDS_MSG_TYPE"] = 'cosmos-sdk/MsgWithdrawDelegationReward'

# // Accounts
# export const CREATE_SUB_ACCOUNT_MSG_TYPE = 'subaccount/MsgCreateSubAccountV1'
# export const ACTIVATE_SUB_ACCOUNT_MSG_TYPE = 'subaccount/MsgActivateSubAccountV1'

# // Profile
message_types["UPDATE_PROFILE_MSG_TYPE"] = 'profile/MsgUpdateProfile'


# // Gov
# export const SUBMIT_PROPOSAL_TYPE = 'cosmos-sdk/MsgSubmitProposal'
# export const DEPOSIT_PROPOSAL_TYPE = 'cosmos-sdk/MsgDeposit'
# export const VOTE_PROPOSAL_TYPE = 'cosmos-sdk/MsgVote'

# // AMM
# export const ADD_LIQUIDITY_MSG_TYPE = 'liquiditypool/AddLiquidity'
# export const REMOVE_LIQUIDITY_MSG_TYPE = 'liquiditypool/RemoveLiquidity'
# export const CREATE_POOL_MSG_TYPE = 'liquiditypool/CreatePool'
# export const CREATE_POOL_WITH_LIQUIDITY_MSG_TYPE = 'liquiditypool/CreatePoolWithLiquidity'
# export const LINK_POOL_MSG_TYPE = 'liquiditypool/LinkPool'
# export const UNLINK_POOL_MSG_TYPE = 'liquiditypool/UnlinkPool'
# export const SET_REWARDS_WEIGHTS_MSG_TYPE = 'liquiditypool/SetRewardsWeights'
# export const SET_REWARD_CURVE_MSG_TYPE = 'liquiditypool/SetRewardCurve'
# export const SET_COMMITMENT_CURVE_MSG_TYPE = 'liquiditypool/SetCommitmentCurve'
# export const STAKE_POOL_TOKEN_MSG_TYPE = 'liquiditypool/StakePoolToken'
# export const UNSTAKE_POOL_TOKEN_MSG_TYPE = 'liquiditypool/UnstakePoolToken'
# export const CLAIM_POOL_REWARDS_MSG_TYPE = 'liquiditypool/ClaimPoolRewards'
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

class UpdateProfileMessage(TypedDict, total = False):
    username: str
    twitter: str
