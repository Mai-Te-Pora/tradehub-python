import itertools
import jsons

from tradehub.public_client import PublicClient as TradehubPublicClient
import tradehub.types as types
from tradehub.utils import sort_and_stringify_json, to_tradehub_asset_amount, format_withdraw_address
from tradehub.wallet import Wallet


class AuthenticatedClient(TradehubPublicClient):

    '''
    TODO
    # AMM reward % -> /get_amm_reward_percentage
    # Vault types -> /get_vault_types
    # Vaults by address -> /get_vaults?address=${address}
    '''

    def __init__(self, wallet: Wallet, node_ip: str, node_port: int = 5001, network: str = "testnet"):
        """
        """
        TradehubPublicClient.__init__(self, node_ip = node_ip, node_port = node_port)
        self.wallet = wallet
        self.account_blockchain_dict = self.get_account_details()
        self.account_nbr = self.account_blockchain_dict["result"]["value"]["account_number"]
        self.account_sequence_nbr = self.account_blockchain_dict["result"]["value"]["sequence"]
        self.network_variables = {
            "testnet": {"chain_id": "switcheochain",},
            "mainnet": {"chain_id": "switcheo-tradehub-1",},
        }
        self.chain_id = self.network_variables[network]["chain_id"]
        self.fees = self.get_transactions_fees()
        self.mode = "block"        # Need to automate
        self.gas = "100000000000"  # Need to automate
        self.tokens = self.get_token_details()


    ## Authenticated Client Getters
    def get_account_details(self):
        return self.get_account(swth_address = self.wallet.address)

    def get_transaction_fee_type(self, transaction_type: str):
        return types.fee_types[transaction_type]

    def set_message_standards(self, messages: list):
        messages_list = []
        for message in messages:
            if hasattr(message, 'originator') and message.originator in [None, ""]:
                message.originator = self.wallet.address
            message_json = jsons.dump(message)
            message_dict = {}
            for key, value in message_json.items():
                if message_json[key] is not None:
                    message_dict[key] = value
            messages_list.append(message_dict)
        return messages_list


    def set_transaction_standards(self, messages: list, transaction_type: str, fee: dict):
        messages_list = self.set_message_standards(messages = messages)
        transaction_type = types.transaction_types[transaction_type]
        transactions_list = [transaction_type] * len(messages_list)
        if fee:
            fee_dict = fee
        else:
            fee_type = self.get_transaction_fee_type(transaction_type)
            fee_amount = self.fees[fee_type] * len(messages)
            fee_dict = {
                "amount": [{"amount": fee_amount, "denom": "swth"}],
                "gas": self.gas,
            }
        return messages_list, transactions_list, fee_dict


    ## Authenticated Client Message Signing, Construction, and Broadcasting
    def sign_transaction(self,
                         messages: list,
                         transaction_types: list,
                         sequence: int = None,
                         memo: str = None,
                         mode: str = None,
                         fee: dict = None):   # Not clear to me if sequnce or mode are necessary here since they are part of the class
        # if self.useSequenceCounter === true:
        #     return self.seqSignAndBroadcast(msgs, types, options)

        # const options = { sequence: currSequence, memo, mode: 'block', fee }
        # fee = {"amount": [{"denom": "swth", "amount": fee_amount}], "gas": gas,}

        '''
            A Signature has the following sequence.  https://docs.switcheo.org/#/?id=authentication
            (1) Construct a list of dictionaries combining message and message types together. <- construct_concreate_messages
            (2) Sign the list of messages generated in step (1). <- sign_message
            (3) Take the signature from step (2) and create a signature JSON message. <- construct_signatures
            (4) Take the signature JSON from step (3) and wrape it in a transaction JSON message. <- construact_transaction
            (5) Take the transaction JSON from step (4) and create the final layer of the transaction JSON message. <- construct_complete_transaction
        '''

        concrete_messages = self.construct_concrete_messages(messages = messages, transaction_types = transaction_types)
        signature = self.sign_message(messages = concrete_messages, sequence = sequence, memo = memo, fee = fee)
        signatures = self.construct_signatures(signature = signature)
        transaction = self.construct_transaction(message = concrete_messages, signatures = [signatures], fees = fee)
        return self.construct_complete_transaction(transaction = transaction)

    def construct_concrete_messages(self, messages: list, transaction_types: list):  # both of these are lists of strings
        if len(messages) != len(transaction_types):
            # throw new Error('Msg length is not equal to types length')
            pass
        if len(messages) > 100:
            # throw new Error('Cannot broadcast more than 100 messages in 1 transaction')
            pass
        
        concrete_messages = []   # ConcreteMsg[] from JS code -> {type: string, value: object}

        for (message, transaction_type) in zip(messages, transaction_types):
            concrete_messages.append({
                "type": transaction_type,
                "value": message,
            })

        return concrete_messages
    
    def sign_message(self,
                     messages: list,
                     sequence: int = None,
                     memo: str = None,
                     mode: str = None,
                     fee: dict = None):     # JS original -> msgs: ConcreteMsg[], options: any = {}

        if (not sequence and self.account_sequence_nbr is None) or self.account_nbr is None or self.account_nbr == '0':  # no sequence override, get latest from blockchain
            self.account_blockchain_dict = self.get_account()
            self.account_nbr = self.account_blockchain_dict["result"]["value"]["account_number"]
            self.account_sequence_nbr = self.account_blockchain_dict["result"]["value"]["sequence"]
            if self.account_nbr == '0' or self.account_nbr is None:
                raise ValueError('Account number still 0 after refetching. This suggests your account is not initialized with funds.')

        if fee:
            fee_dict = fee
        else:
            fee_amount = to_tradehub_asset_amount(amount = len(messages), decimals = self.tokens["swth"]["decimals"])
            fee_dict = {
                "amount": [{"denom": "swth", "amount": fee_amount}],
                "gas": self.gas,
            }

        constructed_signing_message = {
            "account_number": self.account_nbr,
            "chain_id": self.chain_id,
            "fee": fee_dict,
            "memo": memo if memo else '',
            "msgs": messages,
            "sequence": self.account_sequence_nbr,
        }

        return self.wallet._sign(message = constructed_signing_message)

    def construct_signatures(self, signature: str):
        return {
            "pub_key": {"type": "tendermint/PubKeySecp256k1", "value": self.wallet.base64_public_key},
            "signature": signature,
        }
    
    def construct_transaction(self, message: list, signatures: list, fees: dict, memo: str = None):
        return {
            "fee": fees,
            "msg": message,
            "memo": memo if memo else '',
            "signatures": signatures
        }
    
    def construct_complete_transaction(self, transaction: dict, mode: str = None):
        return {
            "mode": mode if mode else self.mode,
            "tx": transaction,
        }

    def broadcast_transactions(self, transactions: dict):
        return self.request.post(path = '/txs', json_data = transactions)

    def sign_and_broadcast(self, messages: list, transaction_types: list, fee: dict):   # Eventually need to add memo to this.
        '''
            This is the entry point for all signatures in this Class.
            All the signatures should be handled in the Wallet Client to avoid leaking keys.

        '''
        transactions = self.sign_transaction(messages = messages, transaction_types = transaction_types, fee = fee)
        broadcast_response = self.broadcast_transactions(transactions = transactions)
        if 'code' not in broadcast_response:
            self.account_sequence_nbr = str(int(self.account_sequence_nbr) + 1)
        return broadcast_response

    def submit_transaction_on_chain(self, messages: list, transaction_type: str, fee: dict):
        messages_list, transactions_list, fee_dict = self.set_transaction_standards(messages = messages,
                                                                                    transaction_type = transaction_type,
                                                                                    fee = fee)
        return self.sign_and_broadcast(messages = messages_list, transaction_types = transactions_list, fee = fee_dict)

    ## Authenticated Client Functions
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
        return self.submit_transaction_on_chain(messages = [message], transaction_type = transaction_type, fee = fee)

    def send_tokens(self, message = types.SendTokensMessage, fee: dict = None):
        transaction_type = "SEND_TOKENS_TYPE"
        if hasattr(message, 'from_address') and message.from_address in [None, ""]:
            message.from_address = self.wallet.address
        amounts = []
        for amount in message.amount:
            formatted_amount = to_tradehub_asset_amount(amount = float(amount.amount), decimals = self.tokens[amount.denom]["decimals"])
            amounts.append(types.SendTokensAmount(amount = formatted_amount, denom = amount.denom))
        message.amount = sorted(amounts, key=lambda x: x.denom.lower())  # When dealing with coin lists in Cosmos it is a requirement that they be ordered by name - https://github.com/cosmos/cosmos-sdk/blob/master/types/coin.go#L215
        return self.submit_transaction_on_chain(messages = [message], transaction_type = transaction_type, fee = fee)
    
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
        return self.create_orders(messages = [message], fee = fee)

    def create_orders(self, messages: [types.CreateOrderMessage], fee: dict = None):
        transaction_type = "CREATE_ORDER_MSG_TYPE"
        return self.submit_transaction_on_chain(messages = messages, transaction_type = transaction_type, fee = fee)

    def cancel_order(self, message: types.CancelOrderMessage, fee: dict = None):
        return self.cancel_orders(messages = [message], fee = fee)

    def cancel_orders(self, messages: [types.CancelOrderMessage], fee: dict = None):
        transaction_type = "CANCEL_ORDER_MSG_TYPE"
        return self.submit_transaction_on_chain(messages = messages, transaction_type = transaction_type, fee = fee)

    def cancel_all(self, message: types.CancelAllMessage, fee: dict = None):
        transaction_type = "CANCEL_ALL_MSG_TYPE"
        return self.submit_transaction_on_chain(messages = [message], transaction_type = transaction_type, fee = fee)

    def stake_switcheo(self, message = types.DelegateTokensMessage, fee: dict = None):
        transaction_type = "DELEGATE_TOKENS_MSG_TYPE"
        message.amount.amount = to_tradehub_asset_amount(amount = float(message.amount.amount), decimals = self.tokens["swth"]["decimals"])
        return self.submit_transaction_on_chain(messages = [message], transaction_type = transaction_type, fee = fee)

    def claim_staking_rewards(self, message = types.WithdrawDelegatorRewardsMessage, fee: dict = None):
        transaction_type = "WITHDRAW_DELEGATOR_REWARDS_MSG_TYPE"
        return self.submit_transaction_on_chain(messages = [message], transaction_type = transaction_type, fee = fee)

    def claim_all_staking_rewards(self, message = types.WithdrawAllDelegatorRewardsParams, fee: dict = None):
        transaction_type = "WITHDRAW_DELEGATOR_REWARDS_MSG_TYPE"
        messages = []
        for validator_address in message.validator_addresses:
            messages.append(types.WithdrawDelegatorRewardsMessage(delegator_address=message.delegator_address,validator_address=validator_address))
        return self.submit_transaction_on_chain(messages = messages, transaction_type = transaction_type, fee = fee)

    def create_withdraw(self, message: types.CreateWithdrawMessage, fee: dict = None):
        message.fee_address = 'swth1prv0t8j8tqcdngdmjlt59pwy6dxxmtqgycy2h7'
        message.to_address = format_withdraw_address(address = message.to_address)
        transaction_type = "CREATE_WITHDRAWAL_TYPE"
        return self.submit_transaction_on_chain(messages = [message], transaction_type = transaction_type, fee = fee)
