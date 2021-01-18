import random

import tradehub.types as types
from tradehub.authenticated_client import AuthenticatedClient as TradehubAuthenticatedClient
from tradehub.utils import to_tradehub_asset_amount, validator_crawler_mp
from tradehub.wallet import Wallet


class DemexClient(object):

    def __init__(self, mnemonic: str, network: str = "testnet"):
        self.wallet = Wallet(mnemonic = mnemonic, network = network)
        self.active_peers = validator_crawler_mp(network = 'main')
        self.active_validators = self.active_peers["active_peers"]
        self.validator_ip = self.active_validators[random.randint(a=0, b=len(self.active_peers)-1)]
        self.tradehub = TradehubAuthenticatedClient(wallet = self.wallet, node_ip = self.validator_ip, network = network)

    def limit_buy(self, pair, quantity, price):
        create_order_msg = types.CreateOrderMessage(market = pair,
                                                    side = "buy",
                                                    quantity = quantity,
                                                    price = price,
                                                    type = "limit")
        return self.tradehub.create_order(message = create_order_msg)

    def limit_sell(self, pair, quantity, price):
        create_order_msg = types.CreateOrderMessage(market = pair,
                                                    side = "sell",
                                                    quantity = quantity,
                                                    price = price,
                                                    type = "limit")
        return self.tradehub.create_order(message = create_order_msg)

    def market_buy(self, pair, quantity):
        create_order_msg = types.CreateOrderMessage(market = pair,
                                                    side = "buy",
                                                    quantity = quantity,
                                                    type = "market")
        return self.tradehub.create_order(message = create_order_msg)

    def market_sell(self, pair, quantity):
        create_order_msg = types.CreateOrderMessage(market = pair,
                                                    side = "sell",
                                                    quantity = quantity,
                                                    type = "market")
        return self.tradehub.create_order(message = create_order_msg)

    def stop_limit_buy(self, pair, price, quantity, stop_price, trigger):
        pass

    def stop_limit_sell(self, pair, price, quantity, stop_price, trigger):
        pass

    def stop_market_buy(self, pair, quantity):
        pass

    def stop_market_sell(self, pair, quantity):
        pass
