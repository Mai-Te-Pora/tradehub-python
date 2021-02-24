"""
Description:
    Public Client for the TradeScan API content you see on Switcheo.org
    Its not required to use your private key to interact with these endpoints to track the blockchain state.
Usage:
    from tradescan.public_client import PublicClient
"""

from tradehub.decentralized_client import NetworkCrawlerClient


class TradescanClient(NetworkCrawlerClient):
    """
    This class allows the user to interact with the TradeScan API including information
    available with validators, tokens, delegators, addresses, and blockchain stats.
    """

    def __init__(self,
                 network: str = 'testnet',
                 trusted_ips: list = None,
                 trusted_uris: list = None):
        """
        :param api_url: The URL for the Switcheo API endpoint.
        :type api_url: str
        """
        if trusted_ips and trusted_uris:
            raise ValueError("Use IP's or URI's, not both!")

        NetworkCrawlerClient.__init__(self, network=network, trusted_ip_list=trusted_ips, trusted_uri_list=trusted_uris)

    def get_address_rewards(self, address):
        if address is not None and isinstance(address, str):
            return self.tradehub_get_request(path='/distribution/delegators/{}/rewards'.format(address))

    def get_address_staking(self, address):
        if address is not None and isinstance(address, str):
            return self.tradehub_get_request(path='/staking/delegators/{}/delegations'.format(address))

    def get_address_trades(self, limit=200, pagination=None, address=None):
        api_params = {}
        if limit is not None and limit <= 1000:
            api_params["limit"] = limit
        if pagination is not None and pagination in [True, False]:
            api_params["pagination"] = pagination
        if address is not None and isinstance(address, str):
            api_params["account"] = address
        return self.tradehub_get_request(path='/get_trades_by_account', params=api_params)

    def get_all_validators(self):
        return self.tradehub_get_request(path='/get_all_validators')

    def get_balance(self, address):
        api_params = {}
        if address is not None and isinstance(address, str):
            api_params["account"] = address
        return self.tradehub_get_request(path='/get_balance', params=api_params)

    def get_block(self, block_nbr=0):
        if block_nbr is not None and isinstance(block_nbr, int) and block_nbr > 0:
            return self.tradehub_get_request(path='/blocks/{}'.format(block_nbr))

    def get_blocks(self, limit=200, pagination=None, validator_address=None):
        api_params = {}
        if limit is not None and limit <= 1000:
            api_params["limit"] = limit
        if pagination is not None and pagination in [True, False]:
            api_params["pagination"] = pagination
        if validator_address is not None:
            api_params["proposer"] = validator_address
        return self.tradehub_get_request(path='/get_blocks', params=api_params)

    def get_block_time(self):
        return self.tradehub_get_request(path='/get_block_time')

    def get_commitment_curve(self):
        return self.tradehub_get_request(path='/get_commitment_curve')

    def get_distribution_parameters(self):
        return self.tradehub_get_request(path='/distribution/parameters')

    def get_external_transfers(self, address):
        api_params = {}
        if address is not None and isinstance(address, str):
            api_params["account"] = address
        return self.tradehub_get_request(path='/get_external_transfers', params=api_params)

    def get_inflation_start_time(self):
        return self.tradehub_get_request(path='/get_inflation_start_time')

    def get_latest_blocks(self):
        return self.tradehub_get_request(path='/blocks/latest')

    def get_liquidity_pools(self):
        return self.tradehub_get_request(path='/get_liquidity_pools')

    def get_liquidations(self):
        return self.tradehub_get_request(path='/get_liquidations')

    def get_markets(self,
                    limit=200,
                    pagination=None,
                    is_settled=None):
        api_params = {}
        if limit is not None and limit <= 1000:
            api_params["limit"] = limit
        if pagination is not None and pagination in [True, False]:
            api_params["pagination"] = pagination
        if is_settled is not None and is_settled in [True, False]:
            api_params["is_settled"] = is_settled
        return self.tradehub_get_request(path='/get_markets', params=api_params)

    def get_orders(self,
                   limit=200,
                   pagination=None,
                   transaction_type=None,
                   block_nbr=None,
                   initiator=None,
                   order_status=None,
                   order_type=None):
        api_params = {}
        if limit is not None and limit <= 1000:
            api_params["limit"] = limit
        if pagination is not None and pagination in [True, False]:
            api_params["pagination"] = pagination
        if transaction_type is not None and transaction_type in self.transaction_types:
            api_params["msg_type"] = transaction_type
        if block_nbr is not None and isinstance(block_nbr, int) and block_nbr > 0:
            api_params["height"] = block_nbr
        if initiator is not None:              # system_derisk, system_adl, system_liquidate
            api_params["initiator"] = initiator
        if order_status is not None:           # open
            api_params["order_status"] = order_status
        if order_type is not None:             # market, liquidation
            api_params["order_type"] = order_type
        return self.tradehub_get_request(path='/get_orders', params=api_params)

    def get_positions(self, address):
        api_params = {}
        if address is not None and isinstance(address, str):
            api_params["account"] = address
        return self.tradehub_get_request(path='/get_positions', params=api_params)

    def get_profile(self, address):
        api_params = {}
        if address is not None and isinstance(address, str):
            api_params["account"] = address
        return self.tradehub_get_request(path='/get_profile', params=api_params)

    def get_reward_curve(self):
        return self.tradehub_get_request(path='/get_reward_curve')

    def get_rich_list(self, token):
        api_params = {}
        if token is not None and token.lower() in self.tokens:
            api_params["token"] = token.lower()
        return self.tradehub_get_request(path='/get_rich_list', params=api_params)

    def get_staking_pool(self):
        return self.tradehub_get_request(path='/staking/pool')

    def get_token(self, token):
        api_params = {}
        if token is not None and token.lower() in self.tokens:
            api_params["token"] = token.lower()
        return self.tradehub_get_request(path='/token', params=api_params)

    def get_token_list(self):
        token_list = []
        tokens = self.get_tokens()
        for token in tokens:
            token_list.append(token["denom"])
        return token_list

    def get_tokens(self):
        return self.tradehub_get_request(path='/get_tokens')

    def get_total_balances(self):
        return self.tradehub_get_request(path='/get_total_balances')

    def get_tradehub_monitor(self):
        return self.tradehub_get_request(path='/monitor')

    def get_transaction(self, transaction_hash=None):
        api_params = {}
        if transaction_hash is not None and isinstance(transaction_hash, str):
            api_params["hash"] = transaction_hash
        return self.tradehub_get_request(path='/get_transaction', params=api_params)

    def get_transaction_fees(self):
        return self.tradehub_get_request(path='/get_txns_fees')

    def get_transaction_log(self, transaction_hash=None):
        api_params = {}
        if transaction_hash is not None and isinstance(transaction_hash, str):
            api_params["hash"] = transaction_hash
        return self.tradehub_get_request(path='/get_tx_log', params=api_params)

    def get_transaction_types(self):
        return self.tradehub_get_request(path='/get_transaction_types')

    def get_transactions(self,
                         limit=200,
                         pagination=None,
                         address=None,
                         transaction_type=None,
                         block_nbr=None):
        api_params = {}
        if limit is not None and limit <= 1000:
            api_params["limit"] = limit
        if pagination is not None and pagination in [True, False]:
            api_params["pagination"] = pagination
        if address is not None and isinstance(address, str):
            api_params["address"] = address
        if transaction_type is not None and (transaction_type in self.transaction_types or transaction_type == ''):
            api_params["msg_type"] = transaction_type
        if block_nbr is not None and isinstance(block_nbr, int) and block_nbr > 0:
            api_params["height"] = block_nbr
        return self.tradehub_get_request(path='/get_transactions', params=api_params)

    def get_validator_delegations(self, operator_address):
        return self.tradehub_get_request(path='/staking/validators/{}/delegations'.format(operator_address))

    def get_validator_public_nodes(self):
        public_nodes = {}
        tradehub_state = self.get_tradehub_monitor()
        for validator in tradehub_state:
            public_nodes[validator["moniker"]] = validator["ip"]
        return public_nodes

    def get_validator_public_node_ips(self):
        public_node_ips = []
        nodes_dict = self.get_validator_public_nodes()
        for key in nodes_dict.keys():
            public_node_ips.append(nodes_dict[key])
        return public_node_ips

    def get_validator_missed_blocks(self, address=None):
        validators_missed_blocks = {}
        validators_signing_info = self.get_validator_signing_info()["result"]
        for validator_signing_info in validators_signing_info:
            validators_missed_blocks[validator_signing_info["address"]] = validator_signing_info["missed_blocks_counter"]
        print(validators_missed_blocks)
        return validators_missed_blocks[address]

    def get_validator_signing_info(self, limit=100):
        api_params = {}
        if limit is not None and isinstance(limit, int) and limit > 0:
            api_params["limit"] = limit
        return self.tradehub_get_request(path='/slashing/signing_infos', params=api_params)

    def get_validators(self, status=None):
        api_params = {}
        if status is not None and status in ["unbonding", "unbonded"]:
            api_params["status"] = status
        return self.tradehub_get_request(path='/staking/validators', params=api_params)
