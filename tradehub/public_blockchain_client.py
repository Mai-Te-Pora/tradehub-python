from typing import Union, List, Optional
from tradehub.decentralized_client import NetworkCrawlerClient


class PublicBlockchainClient(NetworkCrawlerClient):
    """
    This class allows the user to interact with the TradeScan API including information
    available with validators, tokens, delegators, addresses, and blockchain stats.
    """

    def __init__(self, network: str = "testnet", trusted_ips: Union[None, list] = None, trusted_uris: Union[None, list] = None, is_websocket_client: bool = False):
        """
        Create a public client using IP:Port or URI format.

        Example::
            public_client = PublicClient(trusted_ips=["127.0.0.1"])

            # or use uri method

            public_client = PublicClient(trusted_uris=["https://tradehub-api-server.network/"])

        :param node_ip: ip address off a tradehub node.
        :param node_port: prt off a tradehub node, default 5001.
        :param uri: URI address off tradehub node.
        """
        if trusted_ips and trusted_uris:
            raise ValueError("Use IP's or URI's, not both!")

        NetworkCrawlerClient.__init__(self, network=network, trusted_ip_list=trusted_ips, trusted_uri_list=trusted_uris, is_websocket_client=is_websocket_client)

    def get_all_validators(self) -> List[dict]:
        """
        Get all validators. This includes active, unbonding and unbonded validators.

        Example::

            public_client.get_all_validators()

        The expected return result for this function is as follows::

            [
                {
                "OperatorAddress":"swthvaloper1vwges9p847l9csj8ehrlgzajhmt4fcq4dmg8x0",
                "ConsPubKey":"swthvalconspub1zcjduepqcufdssqqfycjwz2srp42tytrs7gtdkkry9cpspea3zqsjzqd2tps73pr63",
                "Jailed":false,
                "Status":2,
                "Tokens":"22414566.55131922",
                "DelegatorShares":"22414566.55131922",
                "Description":{
                    "moniker":"Devel \u0026 Co",
                    "identity":"c572aef1818379c38996878357c321398165fcf0",
                    "website":"https://gitlab.com/switcheo-utils",
                    "security_contact":"",
                    "details":"..."},
                    "UnbondingHeight":0,
                    "UnbondingCompletionTime":"1970-01-01T00:00:00Z",
                    "Commission":{
                        "commission_rates":{
                            "rate":"0.004200000000000000",
                            "max_rate":"0.200000000000000000",
                            "max_change_rate":"0.010000000000000000"
                        },
                        "update_time":"2020-11-27T20:25:33.45991154Z"
                    },
                    "MinSelfDelegation":"1",
                    "ConsAddress":"swthvalcons1pqnlj0na6k8u9y27j3elrx584mt3380dal0j9s",
                    "ConsAddressByte":"0827F93E7DD58FC2915E9473F19A87AED7189DED",
                    "WalletAddress":"swth1vwges9p847l9csj8ehrlgzajhmt4fcq4sd7gzl",
                    "BondStatus":"bonded"
                },
                ...
            ]

        .. warning::
            The response from this endpoint uses different types off name conventions!
            For example 'MinSelfDelegation' and 'max_change_rate'.

        .. warning::
            This endpoint returns numbers as string(eg. "volume":"2100") or integer(eg. "resolution":5)

        :return: list with validators.
        """
        return self.tradehub_get_request(path='/get_all_validators')

    def get_block(self, block_nbr: int = 1):
        return self.tradehub_get_request(path='/blocks/{}'.format(block_nbr))

    def get_block_time(self) -> str:
        """
        Get the block time in format HH:MM:SS.ZZZZZZ.

        Example::

            public_client.get_block_time()

        The expected return result for this function is as follows::

            "00:00:02.190211"

        .. warning::
            This endpoint returns only a string.

        :return: block time as string.
        """
        return self.tradehub_get_request(path='/get_block_time')

    def get_blocks(self, before_id: Optional[int] = None, after_id: Optional[int] = None, order_by: Optional[str] = None, swth_valcons: Optional[str] = None, limit: Optional[int] = None) -> List[dict]:
        """
        Get latest blocks or request specific blocks.

        Example::

            public_client.get_blocks()

        The expected return result for this function is as follows::

            [
                {
                    "block_height":"6103923",
                    "time":"2021-01-09T14:15:53.071509+01:00",
                    "count":"1",
                    "proposer_address":"swthvalcons17m2ueqqqt8u0jz4rv5kvk4kg0teel4sckytjlc"
                },
                {
                    "block_height":"6103922",
                    "time":"2021-01-09T14:15:50.824548+01:00",
                    "count":"0",
                    "proposer_address":"swthvalcons1zecfdrf22f6syz8xj4vn8jsvsalxdhwl9tlflk"
                },
                ...
            ]

        .. warning:: This endpoint is not well documented in official documents. The parameters are NOT required.

        :param before_id: Before block height(exclusive).
        :param after_id: After block height(exclusive).
        :param order_by: Not specified yet.
        :param swth_valcons: Switcheo tradehub validator consensus starting with 'swthvalcons1' on mainnet and
            'tswthvalcons1' on testnet.
        :param limit: Limit the responded result. Values greater than 200 have no effect and a maximum off 200
            results are returned.
        :return: List with found blocks matching the requested parameters. Can be empty list [].
        """
        api_params = {
            "before_id": before_id,
            "after_id": after_id,
            "order_by": order_by,
            "proposer": swth_valcons,
            "limit": limit
        }

        return self.tradehub_get_request(path='/get_blocks', params=api_params)

    def get_commitment_curve(self):
        return self.tradehub_get_request(path='/get_commitment_curve')

    def get_distribution_parameters(self):
        return self.tradehub_get_request(path='/distribution/parameters')

    def get_inflation_start_time(self):
        return self.tradehub_get_request(path='/get_inflation_start_time')

    def get_insurance_fund_balance(self):
        """

        .. warning::

            This endpoint is not working yet.

        :return:
        """
        # TODO result currently []
        return self.tradehub_get_request(path='/get_insurance_balance')

    def get_latest_blocks(self):
        return self.tradehub_get_request(path='/blocks/latest')

    def get_liquidity_pools(self):
        return self.tradehub_get_request(path='/get_liquidity_pools')

    def get_liquidations(self, before_id: int, after_id: int, order_by: str, limit: int):
        """

        .. warning::

            This endpoint is not working yet.

        :param before_id:
        :param after_id:
        :param order_by:
        :param limit:
        :return:
        """
        # TODO result currently not available
        api_params = {
            "before_id": before_id,
            "after_id": after_id,
            "order_by": order_by,
            "limit": limit
        }
        return self.tradehub_get_request(path='/get_liquidations', params=api_params)

    def get_market(self, market: str) -> dict:
        """
        Get information about a market.

        Example::

            public_client.get_market("swth_eth1")

        The expected return result for this function is as follows::

           {
                "type":"",
                "name":"swth_eth1",
                "display_name":"SWTH_ETH",
                "description":"SWTH/ETH Spot Market",
                "market_type":"spot",
                "base":"swth",
                "base_name":"Switcheo",
                "base_precision":8,
                "quote":"eth1",
                "quote_name":"Ethereum",
                "quote_precision":18,
                "lot_size":"1",
                "tick_size":"0.0000001",
                "min_quantity":"200",
                "maker_fee":"-0.0005",
                "taker_fee":"0.0025",
                "risk_step_size":"0",
                "initial_margin_base":"1",
                "initial_margin_step":"0",
                "maintenance_margin_ratio":"0",
                "max_liquidation_order_ticket":"0",
                "max_liquidation_order_duration":0,
                "impact_size":"0",
                "mark_price_band":0,
                "last_price_protected_band":0,
                "index_oracle_id":"",
                "expiry_time":"1970-01-01T01:00:00+01:00",
                "is_active":true,
                "is_settled":false,
                "closed_block_height":0,
                "created_block_height":0
            }

        .. warning::

            This endpoint is not well documented in official documents.
            The example market swth_eth does not exist on mainnet. The correct market ticker is 'swth_eth1'.
            See get_markets() for correct tickers.

        .. warning::

            This endpoint returns numbers as string(eg. "lot_size":"1") or integer(eg. "base_precision":8).

        .. warning::

            This endpoint returns the same dict structure even the market does not exist with default values!

        :param market: Market ticker used by blockchain (eg. swth_eth1).
        :return:
        """
        api_params = {
            "market": market,
        }
        return self.tradehub_get_request(path='/get_market', params=api_params)

    def get_market_stats(self, market: Optional[str] = None) -> List[dict]:
        """
        Get statistics about one or all markets.

        Example::

            public_client.get_market_stats()

        The expected return result for this function is as follows::

            [
                {
                    "day_high":"0.0000215",
                    "day_low":"0.000021",
                    "day_open":"0.0000211",
                    "day_close":"0.0000212",
                    "day_volume":"436030",
                    "day_quote_volume":"9.2787298",
                    "index_price":"0",
                    "mark_price":"0",
                    "last_price":"0.00212000",
                    "market":"swth_eth1",
                    "market_type":"spot",
                    "open_interest":"0"
                }
                ...
            ]


        :param market: Market ticker used by blockchain (eg. swth_eth1).
        :return: List with market stats as dict
        """
        api_params = {
            "market": market
        }
        return self.tradehub_get_request(path='/get_market_stats', params=api_params)

    def get_markets(self, market_type: Optional[str] = None, is_active: Optional[bool] = None, is_settled: Optional[bool] = None) -> List[dict]:
        """
        Get all markets or filter markets.

        Example::

            public_client.get_markets()

        The expected return result for this function is as follows::

            [
                {
                    "type":"",
                    "name":"swth_eth1",
                    "display_name":"SWTH_ETH",
                    "description":"SWTH/ETH Spot Market",
                    "market_type":"spot",
                    "base":"swth",
                    "base_name":"Switcheo",
                    "base_precision":8,
                    "quote":"eth1",
                    "quote_name":"Ethereum",
                    "quote_precision":18,
                    "lot_size":"1",
                    "tick_size":"0.0000001",
                    "min_quantity":"200",
                    "maker_fee":"-0.0005",
                    "taker_fee":"0.0025",
                    "risk_step_size":"0",
                    "initial_margin_base":"1",
                    "initial_margin_step":"0",
                    "maintenance_margin_ratio":"0",
                    "max_liquidation_order_ticket":"0",
                    "max_liquidation_order_duration":0,
                    "impact_size":"0",
                    "mark_price_band":0,
                    "last_price_protected_band":0,
                    "index_oracle_id":"",
                    "expiry_time":"1970-01-01T01:00:00+01:00",
                    "is_active":true,
                    "is_settled":false,
                    "closed_block_height":0,
                    "created_block_height":0
                },
                ...
            ]

        .. warning::
            This endpoint returns numbers as string(eg. "lot_size":"1") or integer(eg. "base_precision":8)

        :param market_type: type of the market can be 'futures' or 'spot'
        :param is_active: if only active markets should be returned
        :param is_settled: if only settled markets should be returned
        :return: List with returned market stats as dict
        """

        if market_type and market_type not in ['futures', 'spot']:
            raise ValueError(f"Parameter 'market_type' only can be 'futures' or 'spot'. Got {market_type} instead.")

        api_params = {
            "market_type": market_type,
            "is_active": is_active,
            "is_settled": is_settled
        }

        return self.tradehub_get_request(path='/get_markets', params=api_params)

    def get_nodes(self) -> dict:
        """
        """
        # TODO no results yet available
        return self.tradehub_get_request(path='/monitor')

    def get_oracle_result(self, oracle_id: str):
        """

        .. warning::

            This endpoint is not working yet.

        :param oracle_id:
        :return:
        """
        # TODO no results yet available
        api_params = {
            "id": oracle_id
        }
        return self.tradehub_get_request(path='/get_oracle_result', params=api_params)

    def get_oracle_results(self):
        """

        .. warning::

            This endpoint is not working yet.

        :return:
        """
        # TODO no results yet available
        return self.tradehub_get_request(path='/get_oracle_results')

    def get_prices(self, market: Optional[str]) -> dict:
        """
        Get prices off a market.

        Example::

            public_client.get_prices("swth_eth1")

        The expected return result for this function is as follows::

            {
                "last":"207000",
                "index":"0",
                "fair":"0",
                "mark":"0",
                "mark_avg":"0",
                "settlement":"0",
                "fair_index_delta_avg":"0",
                "market":"",
                "marking_strategy":"",
                "index_updated_at":"0001-01-01T00:00:00Z",
                "last_updated_at":"2021-01-09T22:50:59.068526+01:00",
                "block_height":0
            }

        .. warning::

            This endpoint is not well documented in official documents.
            Parameter 'market' is NOT required, but strongly recommended. The return result has an empty 'market' field.

        .. warning::

            This endpoint returns amounts which are NOT human readable values. Consider 'base_precision' and
            'quote_precision' to calculate a multiplication factor = 10 ^ ('base_precision' - 'quote_precision')

        .. warning::

            This endpoint returns numbers as string(eg. "last":"207000") or integer(eg. "block_height":0)

        .. warning::

            This endpoint returns a result even if the market is not known. Result contains default values.

        :param market: Market ticker used by blockchain (eg. swth_eth1).
        :return: Prices as dict
        """
        api_params = {
            "market": market
        }
        return self.tradehub_get_request(path='/get_prices', params=api_params)

    def get_reward_curve(self):
        return self.tradehub_get_request(path='/get_reward_curve')

    def get_rich_list(self, token: str):
        """

        .. warning::
            This endpoint is not working yet.

        :param token:
        :return:
        """
        # TODO responses currently not available
        api_params = {
            "token": token
        }
        return self.tradehub_get_request(path='/get_rich_list', params=api_params)

    def get_staking_pool(self):
        return self.tradehub_get_request(path='/staking/pool')

    def get_status(self) -> dict:
        """
        Return cosmos RPC status endpoint.

        Example::

            public_client.get_status()

        The expected return result for this function is as follows::

            {
              "jsonrpc": "2.0",
              "id": -1,
              "result": {
                "node_info": {
                  "protocol_version": {
                    "p2p": "7",
                    "block": "10",
                    "app": "0"
                  },
                  "id": "f4cee80e4dec5a686139cb82729118e15f7ce19c",
                  "listen_addr": "tcp://0.0.0.0:26656",
                  "network": "switcheo-tradehub-1",
                  "version": "0.33.7",
                  "channels": "4020212223303800",
                  "moniker": "Devel Sentry Node 2",
                  "other": {
                    "tx_index": "on",
                    "rpc_address": "tcp://0.0.0.0:26659"
                  }
                },
                "sync_info": {
                  "latest_block_hash": "4A2C89C105D7864AA74C9DE4752AF5B59E96045EBAF984C69DD447C4524EC36F",
                  "latest_app_hash": "773651392EEDBFF6AEE088F76E7D75F2932B4D9F74CA27D568F706ADFC12B174",
                  "latest_block_height": "6119142",
                  "latest_block_time": "2021-01-09T22:18:52.722611018Z",
                  "earliest_block_hash": "B4AF1F3D3D3FD5795BDDB7A6A2E6CA4E34D06338505D6EC46DD8F99E72ADCDAB",
                  "earliest_app_hash": "",
                  "earliest_block_height": "1",
                  "earliest_block_time": "2020-08-14T07:32:27.856700491Z",
                  "catching_up": false
                },
                "validator_info": {
                  "address": "DCB03C204B7F94765B4ADCE1D8BEE88AA43AE811",
                  "pub_key": {
                    "type": "tendermint/PubKeyEd25519",
                    "value": "1GmDSymN6jTqQlZA2KeyzqknIncGMMrwnnas/DWGNOI="
                  },
                  "voting_power": "0"
                }
              }
            }

        :return: Status as dict
        """
        return self.tradehub_get_request(path='/get_status')

    def get_transaction_types(self) -> List[str]:
        """
        Get transaction types used by tradehub.

        Example::

            public_client.get_transaction_types()

        The expected return result for this function is as follows::

            [
                "submit_proposal",
                "create_pool",
                "set_reward_curve",
                "send",
                ...
            ]

        :return: List with transaction types as strings.
        """
        return self.tradehub_get_request(path='/get_transaction_types')

    def get_transactions_fees(self):
        gas_fees = self.tradehub_get_request(path='/get_txns_fees')
        fees = {}
        for gas_fee in gas_fees["result"]:
            fees[gas_fee["msg_type"]] = gas_fee["fee"]
        return fees

    def get_token(self, denom) -> dict:
        """
        Get information about a token.

        Example::

            public_client.get_token("swth")

        The expected return result for this function is as follows::

            {
                "name":"Switcheo",
                "symbol":"swth",
                "denom":"swth",
                "decimals":8,
                "blockchain":"neo",
                "chain_id":4,
                "asset_id":"32e125258b7db0a0dffde5bd03b2b859253538ab",
                "is_active":true,
                "is_collateral":false,
                "lock_proxy_hash":"17d0f66eca7fcbfddc8d9706f20513bf5d7419cd",
                "delegated_supply":"100000000000000000",
                "originator":"swth1mw90en8tcqnvdjhp64qmyhuq4qasvhy25dpmvw"
            }

        .. warning::

            This endpoint returns numbers as string(eg. "delegated_supply":"100000000000000000") or integer(eg. "decimals":8)


        :param denom: Denom used by tradehub.
        :return: Information about token as dict.
        """
        api_params = {
            "token": denom
        }
        return self.tradehub_get_request(path='/get_token', params=api_params)

    def get_tokens(self) -> List[dict]:
        """
        Get all known tokens on tradehub chain.

        Example::

            public_client.get_tokens()

        The expected return result for this function is as follows::

            [
                {
                    "name":"Switcheo",
                    "symbol":"swth",
                    "denom":"swth",
                    "decimals":8,
                    "blockchain":"neo",
                    "chain_id":4,
                    "asset_id":"32e125258b7db0a0dffde5bd03b2b859253538ab",
                    "is_active":true,
                    "is_collateral":false,
                    "lock_proxy_hash":"17d0f66eca7fcbfddc8d9706f20513bf5d7419cd",
                    "delegated_supply":"100000000000000000",
                    "originator":"swth1mw90en8tcqnvdjhp64qmyhuq4qasvhy25dpmvw"
                },
                ...
            ]

        .. warning::
            This endpoint returns numbers as string(eg. "delegated_supply":"100000000000000000") or integer(eg. "decimals":8)

        :return: List with tokens as dict
        """
        return self.tradehub_get_request(path='/get_tokens')

    def get_token_details(self) -> dict:
        tokens = self.get_tokens()
        tokens_details = {}
        for token in tokens:
            if token["is_active"]:
                tokens_details[token["denom"]] = {
                    'name': token["name"],
                    'symbol': token["symbol"],
                    'decimals': token["decimals"],
                }
        return tokens_details

    def get_top_r_profits(self, market: str, limit: int):
        """

        .. warning::
            This endpoint is not working yet.

        :param market:
        :param limit:
        :return:
        """
        # TODO responses currently not available
        api_params = {
            "market": market,
            "limit": limit
        }
        return self.tradehub_get_request(path='/get_top_r_profits', params=api_params)

    def get_total_balances(self):
        """

        .. warning::
            This endpoint is not working yet.

        :return:
        """
        # TODO responses currently not available
        return self.tradehub_get_request(path='/get_total_balances')

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

    def get_validator_missed_blocks(self):
        validators_missed_blocks = {}
        validators_signing_info = self.get_validator_signing_info()["result"]
        for validator_signing_info in validators_signing_info:
            validators_missed_blocks[validator_signing_info["address"]] = validator_signing_info["missed_blocks_counter"]
        return validators_missed_blocks

    def get_validator_signing_info(self, limit: int = 100):
        api_params = {}
        api_params["limit"] = limit
        return self.tradehub_get_request(path='/slashing/signing_infos', params=api_params)

    def get_validators(self, status: str = None):
        api_params = {}
        if status is not None and status in ["unbonding", "unbonded"]:
            api_params["status"] = status
        return self.tradehub_get_request(path='/staking/validators', params=api_params)

    def get_vault_types(self) -> list:
        """

        :param token:
        :return :
        """
        # TODO responses currently not an empty list
        return self.tradehub_get_request(path='/get_vault_types')

    def get_vaults(self, swth_address: str) -> dict:
        api_params = {
            "address": swth_address,
        }
        return self.tradehub_get_request(path='/get_vaults', params=api_params)
