import itertools

from tradehub.public_client import PublicClient as TradehubPublicClient
from tradehub.types import message_types, fee_types, UpdateProfileMessage
from tradehub.utils import sort_and_stringify_json, to_tradehub_asset_amount
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


    ## Authenticated Client Getters
    def get_account_details(self):
        return self.get_account(swth_address = self.wallet.address)

    def get_transaction_fee_type(self, message_type):
        return fee_types[message_type]


    ## Authenticated Client Message Signing, Construction, and Broadcasting
    def sign_transaction(self,
                         messages: list,
                         message_types: list,
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

        concrete_messages = self.construct_concrete_messages(messages = messages, message_types = message_types)
        print(concrete_messages)
        signature = self.sign_message(messages = concrete_messages, sequence = sequence, memo = memo, fee = fee)
        print(signature)
        signatures = self.construct_signatures(signature = signature)
        print(signatures)
        transaction = self.construct_transaction(message = concrete_messages, signatures = [signatures], fees = fee)
        print(transaction)
        return self.construct_complete_transaction(transaction = transaction)

    def construct_concrete_messages(self, messages: list, message_types: list):  # both of these are lists of strings
        if len(messages) != len(message_types):
            # throw new Error('Msg length is not equal to types length')
            pass
        if len(messages) > 100:
            # throw new Error('Cannot broadcast more than 100 messages in 1 transaction')
            pass
        
        concrete_messages = []   # ConcreteMsg[] from JS code -> {type: string, value: object}

        for (message, message_type) in zip(messages, message_types):
            concrete_messages.append({
                "type": message_type,
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
                print('Account number still 0 after refetching. This suggests your account is not initialized with funds')

        if fee:
            fee_dict = fee
        else:
            fee_amount = to_tradehub_asset_amount(amount = len(messages), power = 8)
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
        
        print(constructed_signing_message)
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
        print(transactions)
        return self.request.post(path = '/txs', json_data = transactions)

    def sign_and_broadcast(self, messages: list, message_types: list, fee: dict):   # Eventually need to add memo to this.
        '''
            This is the entry point for all signatures in this Class.
            All the signatures should be handled in the Wallet Client to avoid leaking keys.

        '''
        transactions = self.sign_transaction(messages = messages, message_types = message_types, fee = fee)
        print(transactions)
        return self.broadcast_transactions(transactions = transactions)

    ## Authenticated Client Functions
    def update_profile(self, message: UpdateProfileMessage, fee: dict = None):
        '''
            message = {
                username: 'PythonAPI',
                twitter: '',
            }
        '''
        if "originator" not in message:
            message["originator"] = self.wallet.address
        message_type = message_types["UPDATE_PROFILE_MSG_TYPE"]
        fee_type = self.get_transaction_fee_type(message_type)
        if fee:
            fee_dict = fee
        else:
            fee_amount = self.fees[fee_type]
            fee_dict = {
                "amount": [{"amount": fee_amount, "denom": "swth"}],
                "gas": self.gas,
            }
        
        return self.sign_and_broadcast(messages = [message], message_types = [message_type], fee = fee_dict)
