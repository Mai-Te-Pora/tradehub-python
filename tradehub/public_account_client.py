from typing import Union, List, Optional
from tradehub.public_blockchain_client import PublicBlockchainClient


class PublicClient(PublicBlockchainClient):
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
        PublicBlockchainClient.__init__(self, network=network, trusted_ips=trusted_ips, trusted_uris=trusted_uris, is_websocket_client=is_websocket_client)

    def check_username(self, username: str) -> dict:
        """

        :param username:
        :return:
        """
        api_params = {
            "username": username,
        }
        return self.tradehub_get_request(path='/username_check', params=api_params)

    def get_account(self, swth_address: str) -> dict:
        """
        Request account information about swth wallet.

        Example::

            # wallet behind Devel And Co validator
            public_client.get_account("swth1vwges9p847l9csj8ehrlgzajhmt4fcq4sd7gzl")

        The expected return result for this function is as follows::

            {
              "height": "6102489",
              "result": {
                "type": "cosmos-sdk/Account",
                "value": {
                  "address": "swth1vwges9p847l9csj8ehrlgzajhmt4fcq4sd7gzl",
                  "coins": [
                    {
                      "denom": "cel1",
                      "amount": "7"
                    },
                    {
                      "denom": "eth1",
                      "amount": "64752601707981"
                    },
                    {
                      "denom": "nex1",
                      "amount": "12289"
                    },
                    {
                      "denom": "nneo2",
                      "amount": "31555"
                    },
                    {
                      "denom": "swth",
                      "amount": "4113439708"
                    },
                    {
                      "denom": "usdc1",
                      "amount": "45376"
                    },
                    {
                      "denom": "wbtc1",
                      "amount": "29"
                    }
                  ],
                  "public_key": {
                    "type": "tendermint/PubKeySecp256k1",
                    "value": "AtCcJkRx1VhzZkOV06yrxKMZ9IvdRxqv5S4gJSQI/aCB"
                  },
                  "account_number": "1756",
                  "sequence": "55"
                }
              }
            }

        .. note:
            This endpoint returns numbers which are NOT human readable values. Consider 'base_precision' and
            'quote_precision' to calculate a multiplication factor = 10 ^ ('base_precision' - 'quote_precision').
            See 'get_markets'

        :param swth_address: tradehub switcheo address starting with 'swth1' on mainnet and 'tswth1' on testnet.
        :return: json response
        """
        api_params = {
            "account": swth_address,
        }
        return self.tradehub_get_request(path='/get_account', params=api_params)

    def get_active_wallets(self, token: str) -> int:
        """

        :param token:
        :return active_wallet_cnt:
        """
        api_params = {
            "token": token,
        }
        return self.tradehub_get_request(path='/get_active_wallets', params=api_params)

    def get_address(self, username: str) -> str:
        """
        Request swth1 tradehub address which is represented by a username.

        Example::

            public_client.get_address("devel484")

        The expected return result for this function is as follows::

            "swth1qlue2pat9cxx2s5xqrv0ashs475n9va963h4hz"

        .. warning::
            This endpoint returns only a string if address is found. If no address is found an exception with
            status code 404 will be raised.

        .. note::
            Usernames are in lowercase and can only be 15 characters long.

        :param username: Username is lower case.
        :return: swth1 address if found
        """
        api_params = {
            "username": username
        }
        return self.tradehub_get_request(path='/get_address', params=api_params)

    def get_address_trades(self, limit: int = 200, pagination: bool = None, address: str = None):
        api_params = {}
        if pagination is not None:
            api_params["pagination"] = pagination
        if address is not None:
            api_params["account"] = address
        return self.tradehub_get_request(path='/get_trades_by_account', params=api_params)

    def get_balance(self, swth_address: str) -> dict:
        """
        Get balance which includes available, in open orders and open positions.

        Example::

            # wallet behind Devel And Co validator
            public_client.get_balance("swth1vwges9p847l9csj8ehrlgzajhmt4fcq4sd7gzl")

        The expected return result for this function is as follows::

            {
                "cel1":{
                    "available":"0.0007",
                    "order":"0",
                    "position":"0",
                    "denom":"cel1"
                },
                "eth1":{
                    "available":"0.000064752601707981",
                    "order":"0",
                    "position":"0",
                    "denom":"eth1"
                },
                "nex1":{
                    "available":"0.00012289",
                    "order":"0",
                    "position":"0",
                    "denom":"nex1"
                },
                "nneo2":{
                    "available":"0.00031555",
                    "order":"0",
                    "position":"0",
                    "denom":"nneo2"
                },
                "swth":{
                    "available":"41.13439708",
                    "order":"0",
                    "position":"0",
                    "denom":"swth"
                },
                "usdc1":{
                    "available":"0.045376",
                    "order":"0",
                    "position":"0",
                    "denom":"usdc1"
                },
                "wbtc1":{
                    "available":"0.00000029",
                    "order":"0",
                    "position":"0",
                    "denom":"wbtc1"
                }
            }

        .. note::
            Only non zero balances are returned.

        .. note::
            Values are already in human readable format.

        :param swth_address: tradehub switcheo address starting with 'swth1' on mainnet and 'tswth1' on testnet.
        :return: dict with currently holding tokens.
        """
        api_params = {
            "account": swth_address
        }
        return self.tradehub_get_request(path='/get_balance', params=api_params)

    def get_candlesticks(self, market: str, granularity: int, from_epoch: int, to_epoch: int) -> List[dict]:
        """
        Get candlesticks for a market.

        Example::

            public_client.get_candlesticks("swth_eth1", 5, 1610203000, 1610203090)

        The expected return result for this function is as follows::

            [
                {
                    "id":38648,
                    "market":"swth_eth1",
                    "time":"2021-01-09T15:35:00+01:00",
                    "resolution":5,
                    "open":"0.0000212",
                    "close":"0.0000212",
                    "high":"0.0000212",
                    "low":"0.0000212",
                    "volume":"2100",
                    "quote_volume":"0.04452"
                },
                ...
            ]


        .. warning::

            This endpoint is not well documented in official documents.
            The example market swth_eth does not exist on mainnet. The correct market ticker is 'swth_eth1'.
            See get_markets() for correct tickers.

        .. warning::

            If any off the required parameters is not provided or incorrect the server responses with 500 status codes.

        .. warning::

            Responses are marked as 'plain' and not as 'text/json'.

        .. warning::

            This endpoint returns numbers as string(ex. "volume":"2100") or integer(ex. "resolution":5)

        :raises ValueError: If 'granularity' is not 1, 5, 30, 60, 360 or 1440.


        :param market: Market ticker used by blockchain (eg. swth_eth1).
        :param granularity: Candlestick period in minutes, possible values are: 1, 5, 30, 60, 360 or 1440.
        :param from_epoch: Start of time range for data in epoch seconds.
        :param to_epoch: End of time range for data in epoch seconds.
        :return: List with candles as dict.
        """
        if granularity not in [1, 5, 30, 60, 360, 1440]:
            raise ValueError("Granularity/Resolution has to be on off the following values: 1, 5, 30, 60, 360 or 1440")

        api_params = {
            "market": market,
            "resolution": granularity,
            "from": from_epoch,
            "to": to_epoch
        }
        return self.tradehub_get_request(path='/candlesticks', params=api_params)

    def get_delegation_rewards(self, swth_address: str) -> dict:
        """
        Request delegation rewards made by a tradehub wallet.

        Example::

            # wallet behind Devel And Co validator
            public_client.get_delegation_rewards("swth1vwges9p847l9csj8ehrlgzajhmt4fcq4sd7gzl")

        The expected return result for this function is as follows::

            {
              "height": "6104998",
              "result": {
                "rewards": [
                  {
                    "validator_address": "swthvaloper1vwges9p847l9csj8ehrlgzajhmt4fcq4dmg8x0",
                    "reward": [
                      {
                        "denom": "swth",
                        "amount": "7928468882.342780820000000000"
                      },
                      ...
                    ]
                  },
                  ...
                ],
                "total": [
                  {
                    "denom": "cel1",
                    "amount": "0.032116540000000000"
                  },
                  ...
                ]
              }
            }

        .. warning::

            Only non zero balances are returned.

        .. warning::

            Values are NOT in human readable format even if the values contain a decimal separator.

        .. warning::

            This endpoint returns amounts which are NOT human readable values. Consider 'base_precision' and
            'quote_precision' to calculate a multiplication factor = 10 ^ ('base_precision' - 'quote_precision')

        .. note::

            This endpoint does not include unclaimed commissions off a validator. If a validator wallet is requested
            only the rewards earned by delegation are returned.

        :param swth_address: tradehub switcheo address starting with 'swth1' on mainnet and 'tswth1' on testnet.
        :return: return dict with generated unclaimed rewards.
        """
        api_params = {
            "account": swth_address,
        }
        return self.tradehub_get_request(path='/get_delegation_rewards', params=api_params)

    def get_external_transfers(self, swth_address: str) -> List[dict]:
        """
        Get external transfers(withdraws or deposits) from other blockchains.

        Example::

            # wallet Devel
            public_client.get_delegation_rewards("swth1qlue2pat9cxx2s5xqrv0ashs475n9va963h4hz")

        The expected return result for this function is as follows::

            [
                {
                    "address":"swth1qlue2pat9cxx2s5xqrv0ashs475n9va963h4hz",
                    "amount":"0.9826",
                    "block_height":5937838,
                    "blockchain":"eth",
                    "contract_hash":"9a016ce184a22dbf6c17daa59eb7d3140dbd1c54",
                    "denom":"eth1",
                    "fee_address":"swth1prv0t8j8tqcdngdmjlt59pwy6dxxmtqgycy2h7",
                    "fee_amount":"0.0174",
                    "id":"12853",
                    "status":"success",
                    "symbol":"ETH",
                    "timestamp":1609839309,
                    "token_name":"Ethereum",
                    "transaction_hash":"",
                    "transfer_type":"deposit"
                },
                ...
            ]

        .. warning::

            This endpoint returns numbers as string(eg. "id":"12853") or integer(eg. "timestamp":1609839309)

        .. note::

            This endpoint return amounts in human readable format.

        :param swth_address: tradehub switcheo address starting with 'swth1' on mainnet and 'tswth1' on testnet.
        :return: List with external transfers
        """
        api_params = {
            "account": swth_address
        }
        return self.tradehub_get_request(path='/get_external_transfers', params=api_params)

    def get_leverage(self, swth_address: str, market: str):
        """

        .. warning::

            This endpoint is not working yet.

        :param swth_address:
        :param market:
        :return:
        """
        # TODO result currently not available
        api_params = {
            "account": swth_address,
            "market": market
        }
        return self.tradehub_get_request(path='/get_leverage', params=api_params)

    def get_orderbook(self, market: str, limit: Optional[int] = None):
        """
        Get the orderbook from a market.

        Example::

            public_client.get_orderbook("swth_eth1")

        The expected return result for this function is as follows::

            {
                "asks": [
                    {
                        "price":"0.0000214",
                        "quantity":"49863"
                    },
                    {
                        "price":"0.0000215",
                        "quantity":"49446"
                    },
                    ...
                ],
                "bids": [
                    {
                        "price":"0.0000212",
                        "quantity":"50248"
                    },
                    {
                        "price":"0.0000211",
                        "quantity":"50295"
                    },
                    ...
                ]
            }

        .. warning::

            This endpoint returns an empty 'asks' and 'bids' list if the market is not known.

        :param market: Market ticker used by blockchain (eg. swth_eth1).
        :param limit: Number off returned orders per side(asks, bids).
        :return: Orderbook as 'asks' and 'bids' list
        """
        api_params = {
            "market": market,
            "limit": limit
        }
        return self.tradehub_get_request(path='/get_orderbook', params=api_params)

    def get_order(self, order_id: str) -> dict:
        """
        Get a specific order by id.

        Example::

            public_client.get_order("4F54D2AE0D793F833806109B4278335BF3D392D4096B682B9A27AF9F8A8BCA58")

        The expected return result for this function is as follows::

            {
                "order_id":"4F54D2AE0D793F833806109B4278335BF3D392D4096B682B9A27AF9F8A8BCA58",
                "block_height":6117321,
                "triggered_block_height":0,
                "address":"swth1wmcj8gmz4tszy5v8c0d9lxnmguqcdkw22275w5",
                "market":"eth1_usdc1",
                "side":"buy",
                "price":"1255.68",
                "quantity":"0.01",
                "available":"0.01",
                "filled":"0",
                "order_status":"open",
                "order_type":"limit",
                "initiator":"amm",
                "time_in_force":"gtc",
                "stop_price":"0",
                "trigger_type":"",
                "allocated_margin_denom":"usdc1",
                "allocated_margin_amount":"0",
                "is_liquidation":false,
                "is_post_only":false,
                "is_reduce_only":false,
                "type":"",
                "block_created_at":"2021-01-09T22:13:34.711571+01:00",
                "username":"",
                "id":"990817"
            }

        :param order_id: Order identified by id
        :return: Order as dict
        """
        api_params = {
            "order_id": order_id
        }
        return self.tradehub_get_request(path='/get_order', params=api_params)

    def get_orders(self, swth_address: Optional[str] = None, before_id: Optional[int] = None,
                   after_id: Optional[int] = None, market: Optional[str] = None, order_type: Optional[str] = None,
                   initiator: Optional[str] = None, order_status: Optional[str] = None, limit: Optional[int] = None) -> List[dict]:
        """
        Request last orders or filter them.

        Example::

            public_client.get_orders()

        The expected return result for this function is as follows::

            [
                {
                    "order_id":"4F54D2AE0D793F833806109B4278335BF3D392D4096B682B9A27AF9F8A8BCA58",
                    "block_height":6117321,
                    "triggered_block_height":0,
                    "address":"swth1wmcj8gmz4tszy5v8c0d9lxnmguqcdkw22275w5",
                    "market":"eth1_usdc1",
                    "side":"buy",
                    "price":"1255.68",
                    "quantity":"0.01",
                    "available":"0.01",
                    "filled":"0",
                    "order_status":"open",
                    "order_type":"limit",
                    "initiator":"amm",
                    "time_in_force":"gtc",
                    "stop_price":"0",
                    "trigger_type":"",
                    "allocated_margin_denom":"usdc1",
                    "allocated_margin_amount":"0",
                    "is_liquidation":false,
                    "is_post_only":false,
                    "is_reduce_only":false,
                    "type":"",
                    "block_created_at":"2021-01-09T22:13:34.711571+01:00",
                    "username":"",
                    "id":"990817"
                },
                ...
            ]

        .. warning::

            This endpoint is not well documented in official documents.
            Parameter account is NOT required! It is possible to provide more parameters,
            known ones are documented here.

        .. warning::

            This endpoint returns numbers as string(eg. "id":"990817") or integer(eg. "block_height":6117321)

        :param swth_address: tradehub switcheo address starting with 'swth1' on mainnet and 'tswth1' on testnet.
        :param before_id: return orders before id(exclusive).
        :param after_id: return orders after id(exclusive).
        :param market: Market ticker used by blockchain (eg. swth_eth1).
        :param order_type: Return specific orders, allowed values: 'limit', 'market', 'stop-market' or 'stop-limit'.
        :param initiator: Filter by user or automated market maker orders, allowed values: 'user' or 'amm'.
        :param order_status: Filter by order status, allowed values: 'open' or 'closed'.
        :param limit: Limit response, values above 200 have no effect.
        :return: List off orders as dict
        """
        api_params = {
            "account": swth_address,
            "before_id": before_id,
            "after_id": after_id,
            "market": market,
            "order_type": order_type,
            "initiator": initiator,
            "order_status": order_status,
            "limit": limit
        }
        return self.tradehub_get_request(path='/get_orders', params=api_params)

    def get_position(self, swth_address: str, market: str):
        """

        .. warning::

            This endpoint is not working yet.

        :param swth_address:
        :param market:
        :return:
        """
        # TODO responses currently not available
        api_params = {
            "account": swth_address,
            "market": market
        }
        return self.tradehub_get_request(path='/get_position', params=api_params)

    def get_positions(self, swth_address: str):
        """

        .. warning::

            This endpoint is not working yet.

        :param swth_address:
        :return:
        """
        # TODO responses currently not available
        api_params = {
            "account": swth_address
        }
        return self.tradehub_get_request(path='/get_positions', params=api_params)

    def get_positions_sorted_by_pnl(self, market):
        """

        .. warning::

            This endpoint is not working yet.

        :param market:
        :return:
        """
        # TODO responses currently not available
        api_params = {
            "market": market
        }
        return self.tradehub_get_request(path='/get_positions_sorted_by_pnl', params=api_params)

    def get_positions_sorted_by_risk(self, market):
        """

        .. warning::

            This endpoint is not working yet.

        :param market:
        :return:
        """
        # TODO responses currently not available
        api_params = {
            "market": market
        }
        return self.tradehub_get_request(path='/get_positions_sorted_by_risk', params=api_params)

    def get_positions_sorted_by_size(self, market):
        """

        .. warning::

            This endpoint is not working yet.

        :param market:
        :return:
        """
        # TODO responses currently not available
        api_params = {
            "market": market
        }
        return self.tradehub_get_request(path='/get_positions_sorted_by_size', params=api_params)

    def get_profile(self, swth_address: str) -> dict:
        """
        Get profile from a tradehub wallet.

        Example::

            public_client.get_profile("swth1qlue2pat9cxx2s5xqrv0ashs475n9va963h4hz")

        The expected return result for this function is as follows::

            {
                "address":"swth1qlue2pat9cxx2s5xqrv0ashs475n9va963h4hz",
                "last_seen_block":"6036318",
                "last_seen_time":"2021-01-07T21:47:14.593249+01:00",
                "twitter":"",
                "username":"devel484"
            }

        :param swth_address: tradehub switcheo address starting with 'swth1' on mainnet and 'tswth1' on testnet.
        :return: Profile as dict
        """
        api_params = {
            "account": swth_address
        }
        return self.tradehub_get_request(path='/get_profile', params=api_params)

    def get_trades(self, market: Optional[str] = None, before_id: Optional[int] = None, after_id: Optional[int] = None,
                   order_by: Optional[str] = None, limit: Optional[int] = None,
                   swth_address: Optional[str] = None) -> List[dict]:
        """
        Get recent trades or filter trades.

        Example::

            public_client.get_trades()

        The expected return result for this function is as follows::

            [
                {
                    "id":"103965",
                    "block_created_at":"2021-01-10T21:59:53.563633+01:00",
                    "taker_id":"11DCD0B7B0A0021476B8C801FD627B297EBDBBE7436BFEEC5ADB734DCF3C9291",
                    "taker_address":"swth1qlue2pat9cxx2s5xqrv0ashs475n9va963h4hz",
                    "taker_fee_amount":"0.000007",
                    "taker_fee_denom":"eth1",
                    "taker_side":"buy",
                    "maker_id":"A59962E7A61F361F7DE5BF00D7A6A8225668F449D73301FB9D3787E4C13DEE60",
                    "maker_address":"swth1wmcj8gmz4tszy5v8c0d9lxnmguqcdkw22275w5",
                    "maker_fee_amount":"-0.0000035",
                    "maker_fee_denom":"eth1",
                    "maker_side":"sell",
                    "market":"eth1_usdc1",
                    "price":"1251.51",
                    "quantity":"0.007",
                    "liquidation":"",
                    "taker_username":"devel484",
                    "maker_username":"",
                    "block_height":"6156871"
                },
                ...
            ]


        :param market: Market ticker used by blockchain (eg. swth_eth1).
        :param before_id: get orders before id(exclusive).
        :param after_id: get orders after id(exclusive).
        :param order_by: TODO no official documentation.
        :param limit: limit the responded result, values above 200 have no effect.
        :param swth_address: tradehub switcheo address starting with 'swth1' on mainnet and 'tswth1' on testnet.
        :return: List off trades as dict
        """
        api_params = {
            "market": market,
            "before_id": before_id,
            "after_id": after_id,
            "order_by": order_by,
            "limit": limit,
            "account": swth_address
        }
        return self.tradehub_get_request(path='/get_trades', params=api_params)

    def get_transaction(self, tx_hash: str):
        """
        Get a transaction by providing the hash.

        Example::

            public_client.get_transaction("A93BEAC075562D4B6031262BDDE8B9A720346A54D8570A881E3671FEB6E6EFD4")

        The expected return result for this function is as follows::

            {
                "id":"311003",
                "hash":"A93BEAC075562D4B6031262BDDE8B9A720346A54D8570A881E3671FEB6E6EFD4",
                "address":"swth1vwges9p847l9csj8ehrlgzajhmt4fcq4sd7gzl",
                "username":"",
                "msgs": [
                    {
                        "msg_type":"vote",
                        "msg":"{\"proposal_id\":10,\"voter\":\"swth1vwges9p847l9csj8ehrlgzajhmt4fcq4sd7gzl\",\"option\":\"Yes\"}"
                    },
                    ...
                ],
                "code":"0",
                "gas_used":"64818",
                "gas_limit":"200000",
                "memo":"",
                "height":"6034329",
                "block_time":"2021-01-07T20:35:08.526914+01:00"
            }

        .. warning::

            This endpoint returns the same dict structure even if the transaction does not exist with default values!

        .. note::

            The field 'msg' contain a escaped JSON string.


        :param tx_hash: Transaction hash for a specific transaction.
        :return:
        """
        api_params = {
            "hash": tx_hash
        }
        return self.tradehub_get_request(path='/get_transaction', params=api_params)

    def get_transaction_log(self, transaction_hash: str):
        api_params = {}
        api_params["hash"] = transaction_hash
        return self.tradehub_get_request(path='/get_tx_log', params=api_params)

    def get_transactions(self, swth_address: Optional[str] = None, msg_type: Optional[str] = None,
                         height: Optional[int] = None, start_block: Optional[int] = None,
                         end_block: Optional[int] = None, before_id: Optional[int] = None,
                         after_id: Optional[int] = None, order_by: Optional[str] = None,
                         limit: Optional[int] = None) -> List[dict]:
        """
        Get latest transactions or filter them.

        Example::

            public_client.get_transactions()

        The expected return result for this function is as follows::

            [
                {
                    "id":"322811",
                    "hash":"9742B27016F08484D8FADFD361C34563F3FDA92A36A8DD3B844A2F86E3552451",
                    "address":"swth1xkahzn8ymps6xdu6feulutawu42fkyqz5fgvhx",
                    "username":"",
                    "msg_type":"create_order",
                    "msg":'{\"market\":\"eth1_usdc1\",\"side\":\"buy\",\"quantity\":\"0.019\",\"type\":\"limit\",\"price\":\"1283.98\",\"is_post_only\":false,\"is_reduce_only\":false,\"originator\":\"swth1xkahzn8ymps6xdu6feulutawu42fkyqz5fgvhx\"}',
                    "code":"0",
                    "gas_used":"140666",
                    "gas_limit":"100000000000",
                    "memo":"",
                    "height":"6119373",
                    "block_time":"2021-01-09T23:27:10.247711+01:00"
                },
                ...
            ]

        .. note::

            The field 'msg' contain a escaped JSON string.

        :param swth_address: tradehub switcheo address starting with 'swth1' on mainnet and 'tswth1' on testnet.
        :param msg_type: filter by msg_type, allowed values can be fetch with 'get_transaction_types'
        :param height: get order at a specific height
        :param start_block: get orders after block(exclusive)
        :param end_block: get orders before block(exclusive)
        :param before_id: get orders before id(exclusive)
        :param after_id: get orders after id(exclusive)
        :param order_by: TODO no official documentation
        :param limit: limit the responded result, values above 200 have no effect
        :return: List with transactions as dict
        """
        api_params = {
            "address": swth_address,
            "msg_type": msg_type,
            "height": height,
            "start_block": start_block,
            "end_block": end_block,
            "before_id": before_id,
            "after_id": after_id,
            "order_by": order_by,
            "limit": limit
        }
        return self.tradehub_get_request(path='/get_transactions', params=api_params)

    def get_username_check(self, username: str) -> bool:
        """
        Check if a username is taken or not.

         Example::

            public_client.get_username_check("devel484")

        The expected return result for this function is as follows::

            true

        .. warning::
            This endpoint do not return a JSON response, only true or false

        :param username: name to check
        :return: True if is taken and false if free
        """
        api_params = {
            "username": username
        }
        return self.tradehub_get_request(path='/username_check', params=api_params)
