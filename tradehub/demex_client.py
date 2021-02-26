"""
Description:

    Demex Client for the Switcheo Tradehub decentralized exchange.
    This is the client that you should use to start trading with Demex.
    You will find the necessary trading functions to trade on the exchange that you would find in the UI.
    To get started you will need to use your mnemonic to access your wallet and define the network you want to use.

Usage::

    from tradehub.demex_client import DemexClient
"""
from decimal import Decimal

import tradehub.types as types
from tradehub.authenticated_client import AuthenticatedClient as TradehubAuthenticatedClient
from tradehub.wallet import Wallet


class DemexClient(object):
    """
    This class allows the user to interact with the Demex API to manage and trade the users Tradehub account.
    Execution of this function is as follows::

        DemexClient(mnemonic='lorem ipsum dolor consectetur adipiscing eiusmod tempor incididunt labore magna',
                    network='mainnet',
                    trusted_ips=None,
                    trusted_uris=['http://175.41.151.35:5001', 'http://54.255.5.46:5001'])
    """

    def __init__(self, mnemonic: str, network: str = "testnet", trusted_ips: list = None, trusted_uris: list = None):
        """
        :param mnemonic: The 12 or 24 word seed required to access your wallet and trade on Demex
        :type mnemonic: str
        :param network: The network you want to interact with. Accepts "testnet" or "mainnet".
        :type network: str
        :param trusted_ips: A list of Validator IP addresses that the user trusts, providing this value bypasses the network crawler.
        :type trusted_ips: list
        :param trusted_uris: A list of Validator URIs that the user trusts, providing this value bypasses the network crawler.
        :type trusted_uris: list
        """
        self.wallet = Wallet(mnemonic=mnemonic, network=network)
        self.tradehub = TradehubAuthenticatedClient(wallet=self.wallet, network=network, trusted_ips=trusted_ips, trusted_uris=trusted_uris)

    def limit_buy(self, pair: str, quantity: str, price: str):
        """
        Function to place a limit buy order on Demex.

        Execution of this function is as follows::

            limit_buy(pair='swth_eth1', quantity=1000, price='0.0001')

        The expected return result for this function is as follows::

            {
                'height': str,
                'txhash': str,
                `'raw_log': str,
                'logs': [{
                    'msg_index': int,
                    'log': str,
                    'events': [{
                        'type': str,
                        'attributes': [{
                            'key': str,
                            'value': str
                        }, {
                            'key': str,
                            'value': str
                        }]
                    }]
                }],
                'gas_wanted': str,
                'gas_used': str
            }

        :return: Dictionary in the form of a JSON message with the limit order details.
        """
        create_order_msg = types.CreateOrderMessage(market=pair,
                                                    side="buy",
                                                    quantity=quantity,
                                                    price=price,
                                                    type="limit")
        return self.tradehub.create_order(message=create_order_msg)

    def limit_sell(self, pair: str, quantity: str, price: str):
        """
        Function to place a limit sell order on Demex.

        Execution of this function is as follows::

            limit_sell(pair='swth_eth1', quantity=1000, price='0.0002')

        The expected return result for this function is as follows::

            {
                'height': str,
                'txhash': str,
                `'raw_log': str,
                'logs': [{
                    'msg_index': int,
                    'log': str,
                    'events': [{
                        'type': str,
                        'attributes': [{
                            'key': str,
                            'value': str
                        }, {
                            'key': str,
                            'value': str
                        }]
                    }]
                }],
                'gas_wanted': str,
                'gas_used': str
            }

        :return: Dictionary in the form of a JSON message with the limit order details.
        """
        create_order_msg = types.CreateOrderMessage(market=pair,
                                                    side="sell",
                                                    quantity=quantity,
                                                    price=price,
                                                    type="limit")
        return self.tradehub.create_order(message=create_order_msg)

    def market_buy(self, pair: str, quantity: str):
        """
        Function to place a market buy order on Demex.

        Execution of this function is as follows::

            market_buy(pair='swth_eth1', quantity=1000)

        The expected return result for this function is as follows::

            {
                'height': str,
                'txhash': str,
                `'raw_log': str,
                'logs': [{
                    'msg_index': int,
                    'log': str,
                    'events': [{
                        'type': str,
                        'attributes': [{
                            'key': str,
                            'value': str
                        }, {
                            'key': str,
                            'value': str
                        }]
                    }]
                }],
                'gas_wanted': str,
                'gas_used': str
            }

        :return: Dictionary in the form of a JSON message with the market order details.
        """
        create_order_msg = types.CreateOrderMessage(market=pair,
                                                    side="buy",
                                                    quantity=quantity,
                                                    type="market")
        return self.tradehub.create_order(message=create_order_msg)

    def market_sell(self, pair: str, quantity: str):
        """
        Function to place a market sell order on Demex.

        Execution of this function is as follows::

            market_sell(pair='swth_eth1', quantity=1000)

        The expected return result for this function is as follows::

            {
                'height': str,
                'txhash': str,
                `'raw_log': str,
                'logs': [{
                    'msg_index': int,
                    'log': str,
                    'events': [{
                        'type': str,
                        'attributes': [{
                            'key': str,
                            'value': str
                        }, {
                            'key': str,
                            'value': str
                        }]
                    }]
                }],
                'gas_wanted': str,
                'gas_used': str
            }

        :return: Dictionary in the form of a JSON message with the market order details.
        """
        create_order_msg = types.CreateOrderMessage(market=pair,
                                                    side="sell",
                                                    quantity=quantity,
                                                    type="market")
        return self.tradehub.create_order(message=create_order_msg)

    def stop_limit_buy(self, pair: str, price: str, quantity: str, stop_price: str):
        """
        Function to place a stop limit buy order on Demex.

        Execution of this function is as follows::

            stop_limit_buy(pair='swth_eth1', quantity=1000, price='0.0001', stop_price='0.00015')

        The expected return result for this function is as follows::

            {
                'height': str,
                'txhash': str,
                `'raw_log': str,
                'logs': [{
                    'msg_index': int,
                    'log': str,
                    'events': [{
                        'type': str,
                        'attributes': [{
                            'key': str,
                            'value': str
                        }, {
                            'key': str,
                            'value': str
                        }]
                    }]
                }],
                'gas_wanted': str,
                'gas_used': str
            }

        :return: Dictionary in the form of a JSON message with the stop limit order details.
        """
        current_price = self.tradehub.get_prices(market=pair)["last"]
        if Decimal(stop_price) > Decimal(current_price):
            create_order_msg = types.CreateOrderMessage(market=pair,
                                                        side="buy",
                                                        quantity=quantity,
                                                        price=price,
                                                        type="stop-limit",
                                                        stop_price=stop_price,
                                                        trigger_type="last_price")
            return self.tradehub.create_order(message=create_order_msg)
        else:
            raise ValueError("Stop Price target {} is required to be higher than the current market price {} to trigger a stop order.".format(stop_price, current_price))

    def stop_limit_sell(self, pair: str, price: str, quantity: str, stop_price: str):
        """
        Function to place a stop limit sell order on Demex.

        Execution of this function is as follows::

            stop_limit_sell(pair='swth_eth1', quantity=1000, price='0.0002', stop_price='0.00015')

        The expected return result for this function is as follows::

            {
                'height': str,
                'txhash': str,
                `'raw_log': str,
                'logs': [{
                    'msg_index': int,
                    'log': str,
                    'events': [{
                        'type': str,
                        'attributes': [{
                            'key': str,
                            'value': str
                        }, {
                            'key': str,
                            'value': str
                        }]
                    }]
                }],
                'gas_wanted': str,
                'gas_used': str
            }

        :return: Dictionary in the form of a JSON message with the stop limit order details.
        """
        current_price = self.tradehub.get_prices(market=pair)["last"]
        if Decimal(stop_price) < Decimal(current_price):
            create_order_msg = types.CreateOrderMessage(market=pair,
                                                        side="sell",
                                                        quantity=quantity,
                                                        price=price,
                                                        type="stop-limit",
                                                        stop_price=stop_price,
                                                        trigger_type="last_price")
            return self.tradehub.create_order(message=create_order_msg)
        else:
            raise ValueError("Stop Price target {} is required to be below the current market price {} to trigger a stop order.".format(stop_price, current_price))

    def stop_market_buy(self, pair: str, quantity: str, stop_price: str):
        """
        Function to place a stop market buy order on Demex.

        Execution of this function is as follows::

            stop_market_buy(pair='swth_eth1', quantity=1000, stop_price='0.00015')

        The expected return result for this function is as follows::

            {
                'height': str,
                'txhash': str,
                `'raw_log': str,
                'logs': [{
                    'msg_index': int,
                    'log': str,
                    'events': [{
                        'type': str,
                        'attributes': [{
                            'key': str,
                            'value': str
                        }, {
                            'key': str,
                            'value': str
                        }]
                    }]
                }],
                'gas_wanted': str,
                'gas_used': str
            }

        :return: Dictionary in the form of a JSON message with the stop market order details.
        """
        current_price = self.tradehub.get_prices(market=pair)["last"]
        if Decimal(stop_price) > Decimal(current_price):
            create_order_msg = types.CreateOrderMessage(market=pair,
                                                        side="buy",
                                                        quantity=quantity,
                                                        type="stop-market",
                                                        stop_price=stop_price,
                                                        trigger_type="last_price")
            return self.tradehub.create_order(message=create_order_msg)
        else:
            raise ValueError("Stop Price target {} is required to be higher than the current market price {} to trigger a stop order.".format(stop_price, current_price))

    def stop_market_sell(self, pair: str, quantity: str, stop_price: str):
        """
        Function to place a stop market sell order on Demex.

        Execution of this function is as follows::

            stop_market_sell(pair='swth_eth1', quantity=1000, stop_price='0.00015')

        The expected return result for this function is as follows::

            {
                'height': str,
                'txhash': str,
                `'raw_log': str,
                'logs': [{
                    'msg_index': int,
                    'log': str,
                    'events': [{
                        'type': str,
                        'attributes': [{
                            'key': str,
                            'value': str
                        }, {
                            'key': str,
                            'value': str
                        }]
                    }]
                }],
                'gas_wanted': str,
                'gas_used': str
            }

        :return: Dictionary in the form of a JSON message with the stop market order details.
        """
        current_price = self.tradehub.get_prices(market=pair)["last"]
        if Decimal(stop_price) < Decimal(current_price):
            create_order_msg = types.CreateOrderMessage(market=pair,
                                                        side="sell",
                                                        quantity=quantity,
                                                        type="stop-market",
                                                        stop_price=stop_price,
                                                        trigger_type="last_price")
            return self.tradehub.create_order(message=create_order_msg)
        else:
            raise ValueError("Stop Price target {} is required to be below the current market price {} to trigger a stop order.".format(stop_price, current_price))

    def cancel_order(self, order_id: str):
        """
        Function to place a cancel order on Demex.

        Execution of this function is as follows::

            cancel_order(order_id='86BE018C4691E1495DA439647A2246ADFB6101D6292A0C9D365AD88E4A6285B6')

        The expected return result for this function is as follows::

            {
                'height': str,
                'txhash': str,
                `'raw_log': str,
                'logs': [{
                    'msg_index': int,
                    'log': str,
                    'events': [{
                        'type': str,
                        'attributes': [{
                            'key': str,
                            'value': str
                        }, {
                            'key': str,
                            'value': str
                        }]
                    }]
                }],
                'gas_wanted': str,
                'gas_used': str
            }

        :return: Dictionary in the form of a JSON message with the cancel order details.
        """
        cancel_order_msg = types.CancelOrderMessage(id=order_id)
        return self.tradehub.cancel_order(message=cancel_order_msg)

    def cancel_orders(self, order_ids: list):
        """
        Function to place a cancel orders on Demex.

        Execution of this function is as follows::

            cancel_order(order_ids=['86BE018C4691E1495DA439647A2246ADFB6101D6292A0C9D365AD88E4A6285B6'])

        The expected return result for this function is as follows::

            {
                'height': str,
                'txhash': str,
                `'raw_log': str,
                'logs': [{
                    'msg_index': int,
                    'log': str,
                    'events': [{
                        'type': str,
                        'attributes': [{
                            'key': str,
                            'value': str
                        }, {
                            'key': str,
                            'value': str
                        }]
                    }]
                }],
                'gas_wanted': str,
                'gas_used': str
            }

        :return: Dictionary in the form of a JSON message with the cancel orders details.
        """
        cancel_order_msgs = []
        for order_id in order_ids:
            cancel_order_msgs.append(types.CancelOrderMessage(id=order_id))
        return self.tradehub.cancel_orders(messages=cancel_order_msgs)

    def cancel_all_open_orders_for_pair(self, pair: str):
        """
        Function to place a cancel all open orders for a trading pair on Demex.

        Execution of this function is as follows::

            cancel_all_open_orders_for_pair(pair='swth_eth1')

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
                        }, {
                            'key': str,
                            'value': str
                        }]
                    }]
                }],
                'gas_wanted': str,
                'gas_used': str
            }

        :return: Dictionary in the form of a JSON message with the cancel all orders for pair details.
        """
        cancel_all_order_msg = types.CancelAllMessage(market=pair)
        return self.tradehub.cancel_all(message=cancel_all_order_msg)

    def edit_orders(self, orders: [types.EditOrderMessage]):
        return self.tradehub.edit_orders(messages=orders)

    def edit_limit_order(self, order_id: str, quantity: str = None, price: str = None):
        """
        Function to edit an open limit order on Demex.

        Execution of this function is as follows::

            edit_limit_order(order_id='86BE018C4691E1495DA439647A2246ADFB6101D6292A0C9D365AD88E4A6285B6',
                             quantity='10000',
                             price='0.00011')

        The expected return result for this function is as follows::

            {
                'height': str,
                'txhash': str,
                `'raw_log': str,
                'logs': [{
                    'msg_index': int,
                    'log': str,
                    'events': [{
                        'type': str,
                        'attributes': [{
                            'key': str,
                            'value': str
                        }, {
                            'key': str,
                            'value': str
                        }]
                    }]
                }],
                'gas_wanted': str,
                'gas_used': str
            }

        :return: Dictionary in the form of a JSON message with the edit limit order details.
        """
        if order_id in self.get_open_limit_orders():
            edit_order_msg = types.EditOrderMessage(id=order_id,
                                                    quantity=quantity,
                                                    price=price)
            return self.tradehub.edit_order(message=edit_order_msg)
        else:
            raise ValueError("The Order ID - {} - is not a valid limit order; is open or a stop or leveraged order?".format(order_id))

    def edit_stop_order(self, order_id: str, quantity: str = None, price: str = None, stop_price: str = None):
        """
        Function to edit an open stop order on Demex.

        Execution of this function is as follows::

            edit_stop_order(order_id='86BE018C4691E1495DA439647A2246ADFB6101D6292A0C9D365AD88E4A6285B6',
                            quantity='10000',
                            price='0.00011')

        The expected return result for this function is as follows::

            {
                'height': str,
                'txhash': str,
                `'raw_log': str,
                'logs': [{
                    'msg_index': int,
                    'log': str,
                    'events': [{
                        'type': str,
                        'attributes': [{
                            'key': str,
                            'value': str
                        }, {
                            'key': str,
                            'value': str
                        }]
                    }]
                }],
                'gas_wanted': str,
                'gas_used': str
            }

        :return: Dictionary in the form of a JSON message with the edit stop order details.
        """
        if order_id in self.get_open_stop_orders():
            edit_order_msg = types.EditOrderMessage(id=order_id,
                                                    quantity=quantity,
                                                    price=price,
                                                    stop_price=stop_price)
            return self.tradehub.edit_order(message=edit_order_msg)
        else:
            raise ValueError("The Order ID - {} - is not a valid stop order; is open or a limit or leveraged order?".format(order_id))

    def get_open_orders(self):
        """
        Function to get all open orders for the wallet attached to the Demex Client.

        Execution of this function is as follows::

            get_open_orders()

        The expected return result for this function is as follows::

            [
                '86BE018C4691E1495DA439647A2246ADFB6101D6292A0C9D365AD88E4A6285B6',
                ...
            ]

        :return: List of order IDs.
        """
        orders = self.tradehub.get_orders(swth_address=self.wallet.address, order_status='open')
        order_dict = {}
        for order in orders:
            order_dict[order["order_id"]] = order
        return order_dict

    def get_open_orders_by_pair(self, pair: str):
        """
        Function to get all open orders for a specific pair for the wallet attached to the Demex Client.

        Execution of this function is as follows::

            get_open_orders(pair='swth_eth1')

        The expected return result for this function is as follows::

            [
                '86BE018C4691E1495DA439647A2246ADFB6101D6292A0C9D365AD88E4A6285B6',
                ...
            ]

        :return: List of order IDs.
        """
        orders = self.tradehub.get_orders(swth_address=self.wallet.address, order_status='open', market=pair)
        order_dict = {}
        for order in orders:
            order_dict[order["order_id"]] = order
        return order_dict

    def get_open_limit_orders(self):
        """
        Function to get all open limit orders for the wallet attached to the Demex Client.

        Execution of this function is as follows::

            get_open_limit_orders()

        The expected return result for this function is as follows::

            [
                '86BE018C4691E1495DA439647A2246ADFB6101D6292A0C9D365AD88E4A6285B6',
                ...
            ]

        :return: List of order IDs.
        """
        orders = self.tradehub.get_orders(swth_address=self.wallet.address, order_status='open', order_type='limit')
        order_dict = {}
        for order in orders:
            order_dict[order["order_id"]] = order
        return order_dict

    def get_open_stop_orders(self):
        """
        Function to get all open stop orders for the wallet attached to the Demex Client.

        Execution of this function is as follows::

            get_open_stop_orders()

        The expected return result for this function is as follows::

            [
                '86BE018C4691E1495DA439647A2246ADFB6101D6292A0C9D365AD88E4A6285B6',
                ...
            ]

        :return: List of order IDs.
        """
        triggerred_stops = self.tradehub.get_orders(swth_address=self.wallet.address, order_status='triggered')
        untriggerred_stops = self.tradehub.get_orders(swth_address=self.wallet.address, order_status='untriggered')
        stops = triggerred_stops + untriggerred_stops
        stop_dict = {}
        for stop in stops:
            stop_dict[stop["order_id"]] = stop
        return stop_dict
