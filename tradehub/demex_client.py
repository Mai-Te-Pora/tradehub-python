from decimal import Decimal
import random

import tradehub.types as types
from tradehub.authenticated_client import AuthenticatedClient as TradehubAuthenticatedClient
from tradehub.utils import validator_crawler_mp
from tradehub.wallet import Wallet


class DemexClient(object):

    def __init__(self, mnemonic: str, network: str = "testnet"):
        self.wallet = Wallet(mnemonic=mnemonic, network=network)
        self.active_peers = validator_crawler_mp(network='main')
        self.active_validators = self.active_peers["active_peers"]
        self.validator_ip = self.active_validators[random.randint(a=0, b=len(self.active_peers)-1)]
        self.tradehub = TradehubAuthenticatedClient(wallet=self.wallet, node_ip=self.validator_ip, network=network)

    def limit_buy(self, pair: str, quantity: str, price: str):
        create_order_msg = types.CreateOrderMessage(market=pair,
                                                    side="buy",
                                                    quantity=quantity,
                                                    price=price,
                                                    type="limit")
        return self.tradehub.create_order(message=create_order_msg)

    def limit_sell(self, pair: str, quantity: str, price: str):
        create_order_msg = types.CreateOrderMessage(market=pair,
                                                    side="sell",
                                                    quantity=quantity,
                                                    price=price,
                                                    type="limit")
        return self.tradehub.create_order(message=create_order_msg)

    def market_buy(self, pair: str, quantity: str):
        create_order_msg = types.CreateOrderMessage(market=pair,
                                                    side="buy",
                                                    quantity=quantity,
                                                    type="market")
        return self.tradehub.create_order(message=create_order_msg)

    def market_sell(self, pair: str, quantity: str):
        create_order_msg = types.CreateOrderMessage(market=pair,
                                                    side="sell",
                                                    quantity=quantity,
                                                    type="market")
        return self.tradehub.create_order(message=create_order_msg)

    def stop_limit_buy(self, pair: str, price: str, quantity: str, stop_price: str):
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
        cancel_order_msg = types.CancelOrderMessage(id=order_id)
        return self.tradehub.cancel_order(message=cancel_order_msg)

    def cancel_orders(self, order_ids: list):
        cancel_order_msgs = []
        for order_id in order_ids:
            cancel_order_msgs.append(types.CancelOrderMessage(id=order_id))
        return self.tradehub.cancel_orders(messages=cancel_order_msgs)

    def cancel_all_open_orders_for_pair(self, pair: str):
        cancel_all_order_msg = types.CancelAllMessage(market=pair)
        return self.tradehub.cancel_all(message=cancel_all_order_msg)

    def edit_orders(self, orders: [types.EditOrderMessage]):
        return self.tradehub.edit_orders(messages=orders)

    def edit_limit_order(self, order_id: str, quantity: str = None, price: str = None):
        if order_id in self.get_open_limit_orders():
            edit_order_msg = types.EditOrderMessage(id=order_id,
                                                    quantity=quantity,
                                                    price=price)
            return self.tradehub.edit_order(message=edit_order_msg)
        else:
            raise ValueError("The Order ID - {} - is not a valid limit order; is open or a stop or leveraged order?".format(order_id))

    def edit_stop_order(self, order_id: str, quantity: str = None, price: str = None, stop_price: str = None):
        if order_id in self.get_open_stop_orders():
            edit_order_msg = types.EditOrderMessage(id=order_id,
                                                    quantity=quantity,
                                                    price=price,
                                                    stop_price=stop_price)
            return self.tradehub.edit_order(message=edit_order_msg)
        else:
            raise ValueError("The Order ID - {} - is not a valid stop order; is open or a limit or leveraged order?".format(order_id))

    def get_open_limit_orders(self):
        orders = self.tradehub.get_orders(swth_address=self.wallet.address, order_status='open', order_type='limit')
        order_dict = {}
        for order in orders:
            order_dict[order["order_id"]] = order
        return order_dict

    def get_open_stop_orders(self):
        triggerred_stops = self.tradehub.get_orders(swth_address=self.wallet.address, order_status='triggered')
        untriggerred_stops = self.tradehub.get_orders(swth_address=self.wallet.address, order_status='untriggered')
        stops = triggerred_stops + untriggerred_stops
        stop_dict = {}
        for stop in stops:
            stop_dict[stop["order_id"]] = stop
        return stop_dict
