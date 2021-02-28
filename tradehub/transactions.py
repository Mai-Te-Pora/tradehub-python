"""
Description:

    Transaction Class used as part of the Authenticated Client to standardize how on-chain messages are constructed.
    This client is the basis any on-chain transaction and handles message construction, standards, signing, and broadcasting.

Usage::

    from tradehub.transactions import Transactions
"""
import jsons

from tradehub.public_account_client import PublicClient as TradehubPublicClient
import tradehub.types as types
from tradehub.wallet import Wallet


class Transactions(TradehubPublicClient):
    """
    This class constructs, standardizes, signs, and broadcasts messages to the Tradehub network.

    Execution of this function is as follows::

        Transactions(wallet=Wallet(),
                     trusted_ips=None,
                     trusted_uris=None,
                     network="mainnet")
    """

    def __init__(self, wallet: Wallet, trusted_ips: list = None, trusted_uris: list = None, network: str = "testnet"):
        """
        :param wallet: Wallet class for Tradehub interaction.
        :type wallet: Wallet
        :param trusted_ips: Known and trusted IPs to connect to for your API requests.
        :type trusted_ips: list
        :param trusted_uris: Known and trusted URIs to connect to for your API requests.
        :type trusted_uris: list
        :param network: Network to submit the transaction.
        :type network: str
        """
        TradehubPublicClient.__init__(self, network=network, trusted_ips=trusted_ips, trusted_uris=trusted_uris)
        self.wallet = wallet
        self.account_blockchain_dict = self.get_account_details()
        self.account_nbr = self.account_blockchain_dict["result"]["value"]["account_number"]
        self.account_sequence_nbr = self.account_blockchain_dict["result"]["value"]["sequence"]
        self.network_variables = {
            "testnet": {"chain_id": "switcheochain", },
            "mainnet": {"chain_id": "switcheo-tradehub-1", },
        }
        self.chain_id = self.network_variables[network]["chain_id"]
        self.fees = self.get_transactions_fees()
        self.mode = "block"        # Need to automate
        self.gas = "100000000000"  # Need to automate
        self.tokens = self.get_token_details()

    def get_account_details(self):
        """
        Retrieve Wallet account details required for submitting transactions on Tradehub.

        Execution of this function is as follows::

            get_account_details()

        The expected return result for this function is as follows::

            {
                'height': '1950991',
                'result': {
                    'type': 'cosmos-sdk/Account',
                    'value': {
                        'address': 'tswth1urfldmcspc9nk4w8vcfakxdf2rc5ee4fr2dn76',
                        'coins': [{
                            'denom': 'btc',
                            'amount': '99033160'
                        }, {
                        ...
                        }],
                        'public_key': {
                            'type': 'tendermint/PubKeySecp256k1',
                            'value': 'Ao8h4bhZr1/m8ZEwPaOizNCcIMDX/yqwQh7LXhI77FLW'
                        },
                        'account_number': '56',
                        'sequence': '3195'
                    }
                }
            }

        :return: Dictionary for the current state of the wallet, including sequence number and balances.
        """
        return self.get_account(swth_address=self.wallet.address)

    def get_transaction_fee_type(self, transaction_type: str):
        return types.fee_types[transaction_type]

    def submit_transaction_on_chain(self, messages: list, transaction_type: str, fee: dict):
        """
        This is the function that every function in higher classes should call.
        Every function in the authenticated_client calls this function.
        It standardizes the transaction construction and the signing and broadcasting.

        Execution of this function is as follows::

            submit_transaction_on_chain(messages=[message], transaction_type="UPDATE_PROFILE_MSG_TYPE", fee=None)

        :return: Dictionary for the transaction submitted on-chain.
        """
        messages_list, transactions_list, fee_dict = self.set_transaction_standards(messages=messages,
                                                                                    transaction_type=transaction_type,
                                                                                    fee=fee)
        return self.sign_and_broadcast(messages=messages_list, transaction_types=transactions_list, fee=fee_dict)

    def set_transaction_standards(self, messages: list, transaction_type: str, fee: dict):
        """
        This function sets standards for the messages in the transaction submitted to the chain.
        Fees, Integer precision as string, and Transaction messages are required.

        Execution of this function is as follows::

            submit_transaction_standards(messages=[message], transaction_type="UPDATE_PROFILE_MSG_TYPE", fee=None)

        :return: Three return variables, 1 for each input but run through standardizations.
        """
        messages_list = self.set_message_standards(messages=messages)
        tradehub_transaction_type = types.transaction_types[transaction_type]
        transactions_list = [tradehub_transaction_type] * len(messages_list)
        fee_dict = self.set_fees(transaction_cnt=len(messages), transaction_type=tradehub_transaction_type, fee=fee)
        return messages_list, transactions_list, fee_dict

    def set_message_standards(self, messages: list):
        """
        Standardize messages, adding an originator or takingo ut keys that don't exist.

        Execution of this function is as follows::

            set_message_standards(messages=[message])

        :return: Three return variables, 1 for each input but run through standardizations.
        """
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

    def set_fees(self, transaction_cnt: int, transaction_type: str, fee: dict):
        """
        Standardize, find, and calculate fees for the number of transactions.

        Execution of this function is as follows::

            set_fees(transaction_cnt=1, transaction_type="UPDATE_PROFILE_MSG_TYPE", fee=None)

        :return: Dictionary for the fee's that will be needed for this transaction.
        """
        if fee:
            fee_dict = fee
        else:
            fee_type = self.get_transaction_fee_type(transaction_type)
            fee_amount = str(int(self.fees[fee_type]) * transaction_cnt)
            fee_dict = {
                "amount": [{"amount": fee_amount, "denom": "swth"}],
                "gas": self.gas,
            }
        return fee_dict

    def sign_and_broadcast(self, messages: list, transaction_types: list, fee: dict):   # Eventually need to add memo to this.
        """
        Now that messages are standardized we need to sign the transaction and broadcast it.
        The actual signature part will be handled by the Wallet Client to avoid leaking keys between classes.

        Execution of this function is as follows::

            sign_and_broadcast(messages=messages_list, transaction_types=transactions_list, fee=fee_dict)

        :return: Dictionary for the transaction submitted on-chain.
        """
        transactions = self.sign_transaction(messages=messages, transaction_types=transaction_types, fee=fee)
        broadcast_response = self.broadcast_transactions(transactions=transactions)
        if 'code' not in broadcast_response:
            self.account_sequence_nbr = str(int(self.account_sequence_nbr) + 1)
        return broadcast_response

    def sign_transaction(self,
                         messages: list,
                         transaction_types: list,
                         memo: str = None,
                         fee: dict = None):
        """
        A Signature has the following sequence.  https://docs.switcheo.org/#/?id=authentication
        (1) Construct a list of dictionaries combining message and message types together. <- construct_concrete_messages
        (2) Sign the list of messages generated in step (1). <- sign_message
        (3) Take the signature from step (2) and create a signature JSON message. <- construct_signatures
        (4) Take the signature JSON from step (3) and wrape it in a transaction JSON message. <- construct_transaction
        (5) Take the transaction JSON from step (4) and create the final layer of the transaction JSON message. <- construct_complete_transaction

        Execution of this function is as follows::

            sign_transaction(messages=messages_list, transaction_types=transactions_list, fee=fee_dict)

        :return: Dictionary for a complete transaction message.
        """
        concrete_messages = self.construct_concrete_messages(messages=messages, transaction_types=transaction_types)
        signature = self.sign_message(messages=concrete_messages, memo=memo, fee=fee)
        signatures = self.construct_signatures(signature=signature)
        transaction = self.construct_transaction(message=concrete_messages, signatures=[signatures], fees=fee)
        return self.construct_complete_transaction(transaction=transaction)

    def construct_concrete_messages(self, messages: list, transaction_types: list):  # both of these are lists of strings
        """
        The first step to building a transaction is merging the messages with the transaction types for each.
        Once constructed then each message can be sent off for signature.

        Execution of this function is as follows::

            construct_concrete_messages(messages=messages_list, transaction_types=transactions_list)

        :return: List of dictionaries of messages with transaction types.
        """
        if len(messages) != len(transaction_types):
            raise ValueError('Message length is not equal to transaction types length.')
        if len(messages) > 100:
            raise ValueError('Cannot broadcast more than 100 messages in 1 transaction')

        concrete_messages = []   # ConcreteMsg[] from JS code -> {type: string, value: object}

        for (message, transaction_type) in zip(messages, transaction_types):
            concrete_messages.append({
                "type": transaction_type,
                "value": message,
            })

        return concrete_messages

    def sign_message(self,
                     messages: list,
                     memo: str = None,
                     fee: dict = None):
        """
        Sign the messages constructed in the previous function.

        Execution of this function is as follows::

            sign_message(messages=messages_list, memo=None, fee=None)

        :return: String as a result of the signed messages.
        """
        if self.account_sequence_nbr is None or self.account_nbr is None or self.account_nbr == '0':  # no sequence override, get latest from blockchain
            self.account_blockchain_dict = self.get_account_details()
            self.account_nbr = self.account_blockchain_dict["result"]["value"]["account_number"]
            self.account_sequence_nbr = self.account_blockchain_dict["result"]["value"]["sequence"]
            if self.account_nbr == '0' or self.account_nbr is None:
                raise ValueError('Account number still 0 after refetching. This suggests your account is not initialized with funds.')

        fee_dict = self.set_fees(transaction_cnt=len(messages), transaction_type=messages[0]["type"], fee=fee)

        constructed_signing_message = {
            "account_number": self.account_nbr,
            "chain_id": self.chain_id,
            "fee": fee_dict,
            "memo": memo if memo else '',
            "msgs": messages,
            "sequence": self.account_sequence_nbr,
        }

        return self.wallet._sign(message=constructed_signing_message)

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
        """
        Now that messages are standardized we need to sign the transaction and broadcast it.
        The actual signature part will be handled by the Wallet Client to avoid leaking keys between classes.

        Execution of this function is as follows::

            broadcast_transactions(transactions=transactions)

        The expected return result for this function is as follows::

        {
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

        :return: Dictionary for the transaction submitted on-chain.
        """
        return self.tradehub_post_request(path='/txs', json_data=transactions)
