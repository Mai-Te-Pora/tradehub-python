from typing import Optional, List, Callable
import websockets
import json


class DemexWebsocket:
    """
    DemexWebsocket is a high-level async implementation off the official Tradehub Demex websocket and provides all
    functionalities described in the documentation.
    """

    def __init__(self, uri: str, ping_interval: Optional[int] = 10, ping_timeout: Optional[int] = 30):
        """
        Create a websocket which is complaint with the specification provided by the offical documentation.

        .. see::
            https://docs.switcheo.org/#/?id=websocket

        :param uri: Websocket URI, starting with 'ws://' or 'wss://' e.g. 'ws://85.214.81.155:5000/ws'
        :param ping_interval: Interval for pinging the server in seconds.
        :param ping_timeout: Time after no response for pings are considered as timeout in seconds.
        """
        self._uri: str = uri
        self._ping_interval: int = ping_interval
        self._ping_timeout: int = ping_timeout
        self._websocket: Optional[websockets.WebSocketClientProtocol] = None

    async def subscribe(self, message_id: str, channels: List[str]):
        """
        Subscribe to one or many channels.

        :param message_id: Identifier that will be included in the websocket message response to allow the subscriber to
                           identify which channel the notification is originated from.
        :param channels: List with channels to join.
        :return: None
        """
        await self.send({
            "id": message_id,
            "method": "subscribe",
            "params": {"channels": channels}
        })

    async def unsubscribe(self, message_id: str, channels: List[str]):
        """
        Unsubscribe to one or many channels.

        :param message_id: Identifier that will be included in the websocket message response to allow the subscriber to
                           identify which channel the notification is originated from.
        :param channels: List with channels to leave.
        :return: None
        """
        await self.send({
            "id": message_id,
            "method": "unsubscribe",
            "params": {"channels": channels}
        })

    async def subscribe_leverages(self, message_id: str, swth_address: str):
        """
        Subscribe to wallet specific leverages channel.

        .. warning::
            This channel has not been tested yet.

        :param message_id: Identifier that will be included in the websocket message response to allow the subscriber to
                           identify which channel the notification is originated from.
        :param swth_address: Tradehub wallet address starting with 'swth1' for mainnet and 'tswth1' for testnet.
        :return: None
        """
        # TODO not tested yet
        channel_name: str = f"leverages.{swth_address}"
        await self.subscribe(message_id, [channel_name])

    async def subscribe_market_stats(self, message_id: str):
        """
        Subscribe to market stats.

        Example::

            ws_client.subscribe_market_stats('market_stats')

        The initial channel message is expected as::

            {
                'id':'market_stats',
                'result': ['market_stats']
            }

        The subscription and channel messages are expected as follow::

            {
                'channel': 'market_stats',
                'sequence_number': 484,
                'result': {
                    'cel1_usdc1': {
                        'day_high': '5.97',
                        'day_low': '5.72',
                        'day_open': '5.86',
                        'day_close': '5.74',
                        'day_volume': '414.4',
                        'day_quote_volume': '2429.009',
                        'index_price': '0',
                        'mark_price': '0',
                        'last_price': '5.74',
                        'market': 'cel1_usdc1',
                        'market_type': 'spot',
                        'open_interest': '0'
                    }
                    ...
                }
            }

        :param message_id: Identifier that will be included in the websocket message response to allow the subscriber to
                           identify which channel the notification is originated from.
        :return: None
        """
        channel_name: str = "market_stats"
        await self.subscribe(message_id, [channel_name])

    async def subscribe_books(self, message_id: str, market: str):
        """
        Subscribe to book channel.

        Example::

            ws_client.subscribe_books('orderbook', "swth_eth1')

        The initial channel message is expected as::

            {
                'id':'orderbook',
                'result': ['books.eth1_usdc1', ...]
            }

        The initial subscription message is expected as::

            {
                'channel': 'books.eth1_usdc1',
                'sequence_number': 924,
                'result': [
                    {
                        'market': 'eth1_usdc1',
                        'price': '1797.1',
                        'quantity': '0.02',
                        'side': 'sell',
                        'type': 'new'
                    },
                    ...
                    {
                        'market': 'eth1_usdc1',
                        'price': '1790.1',
                        'quantity': '0.02',
                        'side': 'buy',
                        'type': 'new'
                    }
                    ...
                ]
            }

        The channel update messages are expected as::

            {
                'channel': 'books.eth1_usdc1',
                'sequence_number': 924,
                'result': [
                    {
                        'market': 'eth1_usdc1',
                        'price': '1797.1',
                        'quantity': '0',
                        'side': 'sell',
                        'type': 'delete'
                    },
                    ...
                    {
                        'market':'eth1_usdc1',
                        'price': '1800.18',
                        'quantity': '-0.43',
                        'side': 'sell',
                        'type': 'update'
                    },
                    ...
                    {
                        'market': 'eth1_usdc1',
                        'price': '1114.48',
                        'quantity': '182.716',
                        'side': 'buy',
                        'type': 'new'
                    }
                ]
            }

        .. note::
            The initial message is a snapshot of the current orderbook. The following messages are delta messages to the
            snapshot. Each message has a 'sequence_number'.

            Updates can contain update types: 'new', 'update' or 'delete'. The quantity in a 'update' message can be
            negative indicating a reduction, while positive value means an increment.

            All updates need to be processed in the provided order to maintain an consistent orderbook.

        .. warning::
            The initial snapshot is a partial orderbook with a total of 100 entries!
            Expect receiving updates for orders outside the local managed orderbook.
            Ignore or reconnect to maintain the local orderbook.

        :param message_id: Identifier that will be included in the websocket message response to allow the subscriber to
                           identify which channel the notification is originated from.
        :param market: Tradehub market identifier, e.g. 'swth_eth1'
        :return: None
        """
        channel_name: str = f"books.{market}"
        await self.subscribe(message_id, [channel_name])

    async def subscribe_orders(self, message_id: str, swth_address: str, market: Optional[str] = None):
        """
        Subscribe to orders channel.

        .. note::
            The market identifier is optional and acts as a filter.

        Example::

            ws_client.subscribe_orders('orders', "swth1...abcd')


        The initial channel message is expected as::

            {
                'id':'orders',
                'result': ['orders.swth1...abcd']
            }

        The channel update messages are expected as::

            {
                'channel': 'orders.swth1...abcd',
                'result': [
                    {
                        'order_id': '7CBBF51B75CF2E046726BB...56757D6D502B01F4BB62178DCF',
                        'block_height': 7375724,
                        'triggered_block_height': 0,
                        'address': 'swth1...abcd',
                        'market': 'eth1_wbtc1',
                        'side': 'sell',
                        'price': '0',
                        'quantity': '0.08',
                        'available': '0.08',
                        'filled': '0',
                        'order_status': 'pending',
                        'order_type': 'market',
                        'initiator': 'user',
                        'time_in_force': 'fok',
                        'stop_price': '0',
                        'trigger_type': '',
                        'allocated_margin_denom': 'eth1',
                        'allocated_margin_amount': '0',
                        'is_liquidation': False,
                        'is_post_only': False,
                        'is_reduce_only': False,
                        'type': 'new',
                        'block_created_at': '2021-02-11T20:36:02.244175356Z',
                        'username': '',
                        'id': ''
                    }
                    ...
                ]
            }



        :param message_id: Identifier that will be included in the websocket message response to allow the subscriber to
                           identify which channel the notification is originated from.
        :param swth_address: Tradehub wallet address starting with 'swth1' for mainnet and 'tswth1' for testnet.
        :param market: Tradehub market identifier, e.g. 'swth_eth1'
        :return: None
        """
        if market:
            channel_name: str = f"orders_by_market.{market}.{swth_address}"
        else:
            channel_name: str = f"orders.{swth_address}"
        await self.subscribe(message_id, [channel_name])

    async def subscribe_positions(self, message_id: str, swth_address: str, market: Optional[str] = None):
        """
        Subscribe to positions channel.

        .. note::
            The market identifier is optional and acts as a filter.

        .. warning::
            This channel is not tested yet.

        :param message_id: Identifier that will be included in the websocket message response to allow the subscriber to
                           identify which channel the notification is originated from.
        :param swth_address: Tradehub wallet address starting with 'swth1' for mainnet and 'tswth1' for testnet.
        :param market: Tradehub market identifier, e.g. 'swth_eth1'
        :return: None
        """
        # TODO not tested yet
        if market:
            channel_name: str = f"positions_by_market.{market}.{swth_address}"
        else:
            channel_name: str = f"positions.{swth_address}"
        await self.subscribe(message_id, [channel_name])

    async def subscribe_recent_trades(self, message_id: str, market: str):
        """
        Subscribe to recent trades.

        Example::

            ws_client.subscribe_recent_trades('trades', "swth_eth1')


        The initial channel message is expected as::

            {
                'id': 'trades',
                'result': ['recent_trades.swth_eth1']
            }

        The channel update messages are expected as::

            {
                'channel': 'recent_trades.eth1_usdc1',
                'sequence_number': 812,
                'result': [
                    {
                        'id': '0',
                        'block_created_at': '2021-02-11T20:49:07.095418551Z',
                        'taker_id': '5FF349410F9CF59BED36D412D1223424835342274BC0E504ED0A17EE4B5B0856',
                        'taker_address': 'swth1vaavrkrm7usqg9hcwhqh2hev9m3nryw7aera8p',
                        'taker_fee_amount': '0.00002',
                        'taker_fee_denom': 'eth1',
                        'taker_side': 'buy',
                        'maker_id': '8334A9C97CAEFAF84774AAADB0D5666E7764BA023DF145C8AF90BB6A6862EA2E',
                        'maker_address': 'swth1wmcj8gmz4tszy5v8c0d9lxnmguqcdkw22275w5',
                        'maker_fee_amount': '-0.00001',
                        'maker_fee_denom': 'eth1',
                        'maker_side': 'sell',
                        'market': 'eth1_usdc1',
                        'price': '1797.1',
                        'quantity': '0.02',
                        'liquidation': '',
                        'taker_username': '',
                        'maker_username': '',
                        'block_height': '7376096'
                    },
                    ...
                ]
            }

        .. warning::
            The field 'id' is sometimes '0'. This endpoint/channel does not seem to work correct.

        :param message_id: Identifier that will be included in the websocket message response to allow the subscriber to
                           identify which channel the notification is originated from.
        :param market: Tradehub market identifier, e.g. 'swth_eth1'
        :return: None
        """
        channel_name: str = f"recent_trades.{market}"
        await self.subscribe(message_id, [channel_name])

    async def subscribe_account_trades(self, message_id: str, swth_address: str, market: Optional[str] = None):
        """
        Subscribe to account trades.

        Example::

            ws_client.subscribe_account_trades('account', 'swth...abcd', 'eth1_usdc1')
            # or for all markets
            ws_client.subscribe_account_trades('account', "swth...abcd')


        The initial channel message is expected as::

            {
                'id': 'account',
                'result': ['account_trades_by_market.eth1_usdc1.swth1...abcd']
            }
            # or for all markets
            {
                'id': 'account',
                'result': ['account_trades.swth1...abcd']
            }

        The channel update messages are expected as::

            {
                'channel': 'recent_trades.eth1_usdc1',
                'sequence_number': 812,
                'result': [
                    {
                        'id': '0',
                        'block_created_at': '2021-02-11T20:49:07.095418551Z',
                        'taker_id': '5FF349410F9CF59BED36D412D1223424835342274BC0E504ED0A17EE4B5B0856',
                        'taker_address': 'swth1...taker',
                        'taker_fee_amount': '0.00002',
                        'taker_fee_denom': 'eth1',
                        'taker_side': 'buy',
                        'maker_id': '8334A9C97CAEFAF84774AAADB0D5666E7764BA023DF145C8AF90BB6A6862EA2E',
                        'maker_address': 'swth1...maker',
                        'maker_fee_amount': '-0.00001',
                        'maker_fee_denom': 'eth1',
                        'maker_side': 'sell',
                        'market': 'eth1_usdc1',
                        'price': '1797.1',
                        'quantity': '0.02',
                        'liquidation': '',
                        'taker_username': '',
                        'maker_username': '',
                        'block_height': '7376096'
                    },
                    ...
                ]
            }

        .. note::
            The market identifier is optional and acts as a filter.

        .. warning::
            The field 'id' is '0' all the time. This endpoint/channel does not seem to work correct.

        :param message_id: Identifier that will be included in the websocket message response to allow the subscriber to
                           identify which channel the notification is originated from.
        :param swth_address: Tradehub wallet address starting with 'swth1' for mainnet and 'tswth1' for testnet.
        :param market: Tradehub market identifier, e.g. 'swth_eth1'
        :return: None
        """
        if market:
            channel_name: str = f"account_trades_by_market.{market}.{swth_address}"
        else:
            channel_name: str = f"account_trades.{swth_address}"
        await self.subscribe(message_id, [channel_name])

    async def subscribe_balances(self, message_id: str, swth_address: str):
        """
        Subscribe to wallet specific balance channel.

        Example::

            ws_client.subscribe_balances('balance', "swth1...abcd')


        The initial channel message is expected as::

            {
                'id': 'balance',
                'result': ['balances.swth1...abcd']
            }

        The subscription and channel messages are expected as follow::

            {
                'channel': 'balances.swth1vaavrkrm7usqg9hcwhqh2hev9m3nryw7aera8p',
                'result': {
                    'eth1': {
                        'available': '0.83941506825',
                        'order': '0',
                        'position': '0',
                        'denom': 'eth1'
                    },
                    ...
                }
            }

        :param message_id: Identifier that will be included in the websocket message response to allow the subscriber to
                           identify which channel the notification is originated from.
        :param swth_address: Tradehub wallet address starting with 'swth1' for mainnet and 'tswth1' for testnet.
        :return: None
        """
        channel_name: str = f"balances.{swth_address}"
        await self.subscribe(message_id, [channel_name])

    async def subscribe_candlesticks(self, message_id: str, market: str, granularity: int):
        """
        Subscribe to candlesticks channel.

        Example::

            ws_client.subscribe_candlesticks('candle', "swth_eth1', 1)


        The initial channel message is expected as::

            {
                'id': 'candle',
                'result': ['candlesticks.swth_eth1.1']
            }

        The subscription and channel messages are expected as follow::

            {
                'channel': 'candlesticks.swth_eth1.1',
                'sequence_number': 57,
                'result': {
                    'id': 0,
                    'market':'swth_eth1',
                    'time': '2021-02-17T10:59:00Z',
                    'resolution': 1,
                    'open': '0.000018',
                    'close': '0.000018',
                    'high': '0.000018',
                    'low': '0.000018',
                    'volume': '5555',
                    'quote_volume': '0.09999'
                }
            }

        :param message_id: Identifier that will be included in the websocket message response to allow the subscriber to
                           identify which channel the notification is originated from.
        :param market: Tradehub market identifier, e.g. 'swth_eth1'
        :param granularity: Define the candlesticks granularity. Allowed values: 1, 5, 15, 30, 60, 360, 1440.
        :return: None
        """
        if granularity not in [1, 5, 15, 30, 60, 360, 1440]:
            raise ValueError(f"Granularity '{granularity}' not supported. Allowed values: 1, 5, 15, 30, 60, 360, 1440")
        channel_name: str = f"candlesticks.{market}.{granularity}"
        await self.subscribe(message_id, [channel_name])

    async def get_order_history(self, message_id: str, swth_address: str, market: Optional[str] = None):
        """
        Request up to 200 order histories.

        Example::

            ws_client.get_order_history('order_history', "swth1vaavrkrm7usqg9hcwhqh2hev9m3nryw7aera8p")

        The expected return result for this function is as follows::

            {
                "id": "order_history",
                "result": [
                    {
                        "order_id": "C7D7DDDCFDC68DF2D078CBD8630B657148893AC24CF8DB8F2E23293C6EDC90AD",
                        "block_height": 7561537,
                        "triggered_block_height": 0,
                        "address": "swth1vaavrkrm7usqg9hcwhqh2hev9m3nryw7aera8p",
                        "market": "wbtc1_usdc1",
                        "side": "sell",
                        "price": "0",
                        "quantity": "0.0011",
                        "available": "0",
                        "filled": "0.0011",
                        "order_status": "filled",
                        "order_type": "market",
                        "initiator": "user",
                        "time_in_force": "fok",
                        "stop_price": "0",
                        "trigger_type": "",
                        "allocated_margin_denom": "wbtc1",
                        "allocated_margin_amount": "0",
                        "is_liquidation": false,
                        "is_post_only": false,
                        "is_reduce_only": false,
                        "type": "",
                        "block_created_at": "2021-02-16T08:31:13.225303Z",
                        "username": "",
                        "id": "2315998"
                    },
                    ...
                ]
            }


        .. note::
            The market identifier is optional and acts as a filter.

        :param message_id: Identifier that will be included in the websocket message response to allow the subscriber to
                           identify which channel the notification is originated from.
        :param swth_address: Tradehub wallet address starting with 'swth1' for mainnet and 'tswth1' for testnet.
        :param market: Tradehub market identifier, e.g. 'swth_eth1'
        :return: None
        """
        await self.send({
            "id": message_id,
            "method": "get_order_history",
            "params": {
                "address": swth_address,
                "market": market
            }
        })

    async def get_recent_trades(self, message_id: str, market: str):
        """
        Request up  to 100 recent trades for a market.

        Example::

            ws_client.get_recent_trades('recent_trades', "swth_eth1")

        The expected return result for this function is as follows::

            {
                "id": "recent_trades",
                "sequence_number": 3,
                "result": [
                    {
                        "id": "0",
                        "block_created_at": "2021-02-16T10:21:31.346041707Z",
                        "taker_id": "3F71918F83D84639F505464335FD355105EE63E622CBB819AAFBBAC97368CC7A",
                        "taker_address": "swth1ysezxr46dhd4dzjsswqte35wfm0ml5dxx97aqt",
                        "taker_fee_amount": "3.2475",
                        "taker_fee_denom": "swth",
                        "taker_side": "buy",
                        "maker_id": "343590CF4F54FEB1E2429F60B77CD3BED701A040418AEB914BB41D561E24E7DE",
                        "maker_address": "swth1a5v8pyhkzjjmyw03mh9zqfakwyu0t5wkv0tf66",
                        "maker_fee_amount": "-0.6495",
                        "maker_fee_denom": "swth",
                        "maker_side": "sell",
                        "market": "swth_eth1",
                        "price": "0.0000182",
                        "quantity": "1299",
                        "liquidation": "",
                        "taker_username": "",
                        "maker_username": "",
                        "block_height": "7564715"
                    },
                    ...
                ]
            }

        .. warning::
            The field 'id' is sometimes '0'. This endpoint/channel does not seem to work correct.

        :param message_id: Identifier that will be included in the websocket message response to allow the subscriber to
                           identify which channel the notification is originated from.
        :param market: Tradehub market identifier, e.g. 'swth_eth1'
        :return: None
        """
        await self.send({
            "id": message_id,
            "method": "get_recent_trades",
            "params": {
                "market": market
            }
        })

    async def get_candlesticks(self, message_id: str, market: str, granularity: int,
                               from_epoch: int, to_epoch: int):
        """
        Requests candlesticks for market with granularity.

        Example::

            ws_client.get_candlesticks('recent_trades', "swth_eth1")

        The subscription and channel messages are expected as follow::

            {
                'id': 'candlesticks.swth_eth1.1',
                'sequence_number': 57,
                'result': [
                    {
                        'id': 0,
                        'market':'swth_eth1',
                        'time': '2021-02-17T10:59:00Z',
                        'resolution': 1,
                        'open': '0.000018',
                        'close': '0.000018',
                        'high': '0.000018',
                        'low': '0.000018',
                        'volume': '5555',
                        'quote_volume': '0.09999'
                    }
                ]
            }

        .. note::
            Only candles with non empty volume will be returned. Expect almost none or just a few candles with a low
            granularity.

        :param message_id: Identifier that will be included in the websocket message response to allow the subscriber to
                           identify which channel the notification is originated from.
        :param market: Tradehub market identifier, e.g. 'swth_eth1'
        :param granularity: Define the candlesticks granularity. Allowed values: 1, 5, 15, 30, 60, 360, 1440.
        :param from_epoch: Starting from epoch seconds.
        :param to_epoch: Ending to epoch seconds.
        :return: None
        """
        if granularity not in [1, 5, 15, 30, 60, 360, 1440]:
            raise ValueError(f"Granularity '{granularity}' not supported. Allowed values: 1, 5, 15, 30, 60, 360, 1440")
        await self.send({
            "id": message_id,
            "method": "get_candlesticks",
            "params": {
                "market": market,
                "resolution": str(granularity),
                "from": str(from_epoch),
                "to": str(to_epoch)
            }
        })

    async def get_open_orders(self, message_id: str, swth_address: str, market: Optional[str] = None):
        """
        Request open orders.

        Example::

            ws_client.get_open_orders('open_orders', "swth1p5hjhag5glkpqaj0y0vn3au7x0vz33k0gxuejk")

        The expected return result for this function is as follows::

            {
                "id": "open_orders",
                "result": [
                    {
                        "order_id": "A7C488A6AE25249E90523FCD603236342025340E3DCAE6A6312133905C41794C",
                        "block_height": 7564973,
                        "triggered_block_height": 0,
                        "address": "swth1p5hjhag5glkpqaj0y0vn3au7x0vz33k0gxuejk",
                        "market": "swth_eth1",
                        "side": "sell",
                        "price": "0.0000181",
                        "quantity": "58806",
                        "available": "58806",
                        "filled": "0",
                        "order_status": "open",
                        "order_type": "limit",
                        "initiator": "amm",
                        "time_in_force": "gtc",
                        "stop_price": "0",
                        "trigger_type": "",
                        "allocated_margin_denom": "swth",
                        "allocated_margin_amount": "0",
                        "is_liquidation": false,
                        "is_post_only": false,
                        "is_reduce_only": false,
                        "type": "",
                        "block_created_at": "2021-02-16T10:30:27.079962Z",
                        "username": "",
                        "id": "2316597"
                    },
                    ...
                ]
            }

        .. note::
            The market identifier is optional and acts as a filter.

        :param message_id: Identifier that will be included in the websocket message response to allow the subscriber to
                           identify which channel the notification is originated from.
        :param swth_address: Tradehub wallet address starting with 'swth1' for mainnet and 'tswth1' for testnet.
        :param market: Tradehub market identifier, e.g. 'swth_eth1'
        :return: None
        """
        await self.send({
            "id": message_id,
            "method": "get_open_orders",
            "params": {
                "address": swth_address,
                "market": market
            }
        })

    async def get_account_trades(self, message_id: str, swth_address: str,
                                 market: Optional[str] = None, page: Optional[int] = None):
        """
        Request up to 100 account trades.

        Example::

            ws_client.get_account_trades('account_trades', 'swth1vaavrkrm7usqg9hcwhqh2hev9m3nryw7aera8p')

        The expected return result for this function is as follows::

            {
                "id": "account_trades",
                "result": [
                    {
                        "base_precision": 8,
                        "quote_precision": 6,
                        "fee_precision": 6,
                        "order_id": "C7D7DDDCFDC68DF2D078CBD8630B657148893AC24CF8DB8F2E23293C6EDC90AD",
                        "market": "wbtc1_usdc1",
                        "side": "sell",
                        "quantity": "0.0001",
                        "price": "48745.12",
                        "fee_amount": "0.004875",
                        "fee_denom": "usdc1",
                        "address": "swth1vaavrkrm7usqg9hcwhqh2hev9m3nryw7aera8p",
                        "block_height": "7561537",
                        "block_created_at": "2021-02-16T08:31:13.225303Z",
                        "id": 289733
                    },
                    ...
                ]
            }

        .. note::
            The market identifier is optional and acts as a filter.

        :param message_id: Identifier that will be included in the websocket message response to allow the subscriber to
                           identify which channel the notification is originated from.
        :param swth_address: Tradehub wallet address starting with 'swth1' for mainnet and 'tswth1' for testnet.
        :param market: Tradehub market identifier, e.g. 'swth_eth1'.
        :param page: Used for pagination.
        :return: None
        """
        await self.send({
            "id": message_id,
            "method": "get_account_trades",
            "params": {
                "address": swth_address,
                "market": market,
                "page": str(page) if page else None
            }
        })

    async def get_market_stats(self, message_id: str, market: Optional[str] = None):
        """
        Request market stats.

        Example::

            ws_client.get_market_stats('market_stats')

        The expected return result for this function is as follows::

            {
                "id": "market_stats",
                "result": {
                    "eth1_usdc1": {
                        "day_high": "1818.51",
                        "day_low": "1751.81",
                        "day_open": "1760.07",
                        "day_close": "1788.19",
                        "day_volume": "36.503",
                        "day_quote_volume": "65153.50224",
                        "index_price": "0",
                        "mark_price": "0",
                        "last_price": "1788.19",
                        "market": "eth1_usdc1",
                        "market_type": "spot",
                        "open_interest": "0"
                    },
                    ...
                }
            }

        .. warning::
            Parameter 'market' has no effect. Maybe not intended as parameter. Request will result in all market stats.

        :param message_id: Identifier that will be included in the websocket message response to allow the subscriber to
                           identify which channel the notification is originated from.
        :param market: Tradehub market identifier, e.g. 'swth_eth1'
        :return: None
        """
        # TODO market has no effect
        await self.send({
            "id": message_id,
            "method": "get_market_stats",
            "params": {
                "market": market
            }
        })

    async def get_leverages(self, message_id: str, swth_address: str, market: Optional[str] = None):
        """
        Request leverages.

        .. note::
            The market identifier is optional and acts as a filter.

        .. warning::
            The request method has not been tested yet.

        :param message_id: Identifier that will be included in the websocket message response to allow the subscriber to
                           identify which channel the notification is originated from.
        :param swth_address: Tradehub wallet address starting with 'swth1' for mainnet and 'tswth1' for testnet.
        :param market: Tradehub market identifier, e.g. 'swth_eth1'.
        :return: None
        """
        # TODO not tested yet
        await self.send({
            "id": message_id,
            "method": "get_leverages",
            "params": {
                "address": swth_address,
                "market": market
            }
        })

    async def get_open_positions(self, message_id: str, swth_address: str, market: Optional[str] = None):
        """
        Request open positions.

        .. note::
            The market identifier is optional and acts as a filter.

        .. warning::
            The request method has not been tested yet.

        :param message_id: Identifier that will be included in the websocket message response to allow the subscriber to
                           identify which channel the notification is originated from.
        :param swth_address: Tradehub wallet address starting with 'swth1' for mainnet and 'tswth1' for testnet.
        :param market: Tradehub market identifier, e.g. 'swth_eth1'.
        :return: None
        """
        # TODO not tested yet
        await self.send({
            "id": message_id,
            "method": "get_open_positions",
            "params": {
                "address": swth_address,
                "market": market
            }
        })

    async def get_closed_positions(self, message_id: str, swth_address: str, market: Optional[str] = None):
        """
        Request closed positions.

        .. note::
            The market identifier is optional and acts as a filter.

        .. warning::
            The request method has not been tested yet.

        :param message_id: Identifier that will be included in the websocket message response to allow the subscriber to
                           identify which channel the notification is originated from.
        :param swth_address: Tradehub wallet address starting with 'swth1' for mainnet and 'tswth1' for testnet.
        :param market: Tradehub market identifier, e.g. 'swth_eth1'.
        :return: None
        """
        # TODO not tested yet
        await self.send({
            "id": message_id,
            "method": "get_closed_positions",
            "params": {
                "address": swth_address,
                "market": market
            }
        })

    async def send(self, data: dict):
        """
        Send data to websocket server. Provided data will be translated to json.

        :param data: data as dictionary.
        :return:
        """
        await self._websocket.send(json.dumps(data))

    async def disconnect(self):
        """
        Safely close the websocket connection.

        :return:
        """
        if self._websocket:
            await self._websocket.close()

    async def connect(self,
                      on_receive_message_callback: Callable,
                      on_connect_callback: Optional[Callable] = None,
                      on_error_callback: Optional[Callable] = None):
        """
        Connect to websocket server.

        .. warning::
            Callbacks need to be NON-BLOCKING! Otherwise the PING-PONG coroutine is blocked and the server will close
            the connection. You will not receive any notification about this.

        :param on_receive_message_callback: async callback which is called with the received message as dict.
        :param on_connect_callback: async callback which is called if websocket is connected.
        :param on_error_callback: async callback which is called if websocket has an error.
        :return: None
        """
        try:
            async with websockets.connect(self._uri,
                                          ping_interval=self._ping_interval,
                                          ping_timeout=self._ping_timeout) as websocket:
                self._websocket = websocket

                if on_connect_callback:
                    await on_connect_callback()

                async for message in websocket:
                    data = json.loads(message)
                    await on_receive_message_callback(data)
        except Exception as e:
            if on_error_callback:
                await on_error_callback(e)
            else:
                raise e
