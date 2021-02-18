import random
from tradehub.demex_client import DemexClient
from tests import APITestCase, TRADING_TESTNET_WALLET_MNEMONIC


class TestTradeHubDemexClient(APITestCase):

    def setUp(self) -> None:
        self.demex_client = DemexClient(mnemonic=TRADING_TESTNET_WALLET_MNEMONIC, network='testnet')

    def test_limit_buy(self):
        expect: dict = {
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

        result: dict = self.demex_client.limit_buy(pair='swth_eth', quantity='400', price='0.0000091')
        self.assertDictStructure(expect, result)

    def test_limit_sell(self):
        expect: dict = {
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

        result: dict = self.demex_client.limit_sell(pair='swth_eth', quantity='400', price='0.0000227')
        self.assertDictStructure(expect, result)

    def test_market_buy(self):
        expect: dict = {
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

        result: dict = self.demex_client.market_buy(pair='swth_eth', quantity='400')
        self.assertDictStructure(expect, result)

    def test_market_sell(self):
        expect: dict = {
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

        result: dict = self.demex_client.market_sell(pair='swth_eth', quantity='400')
        self.assertDictStructure(expect, result)

    def test_stop_limit_buy(self):
        expect: dict = {
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

        pair = 'swth_eth'
        current_price = self.demex_client.tradehub.get_prices(market=pair)["last"]
        stop_price = "{:10.8f}".format(float(current_price) + 0.000001)

        result: dict = self.demex_client.stop_limit_buy(pair=pair, quantity='400', price='0.0000091', stop_price=stop_price)
        self.assertDictStructure(expect, result)

    def test_stop_limit_sell(self):
        expect: dict = {
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

        pair = 'swth_eth'
        current_price = self.demex_client.tradehub.get_prices(market=pair)["last"]
        stop_price = "{:10.8f}".format(float(current_price) - 0.000001)

        result: dict = self.demex_client.stop_limit_sell(pair=pair, quantity='400', price='0.0000227', stop_price=stop_price)
        self.assertDictStructure(expect, result)

    def test_stop_market_buy(self):
        expect: dict = {
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

        pair = 'swth_eth'
        current_price = self.demex_client.tradehub.get_prices(market=pair)["last"]
        stop_price = "{:10.8f}".format(float(current_price) + 0.000001)

        result: dict = self.demex_client.stop_market_buy(pair=pair, quantity='400', stop_price=stop_price)
        self.assertDictStructure(expect, result)

    def test_stop_market_sell(self):
        expect: dict = {
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

        pair = 'swth_eth'
        current_price = self.demex_client.tradehub.get_prices(market=pair)["last"]
        stop_price = "{:10.8f}".format(float(current_price) - 0.000001)

        result: dict = self.demex_client.stop_market_sell(pair=pair, quantity='400', stop_price=stop_price)
        self.assertDictStructure(expect, result)

    def test_cancel_order(self):
        expect: dict = {
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

        order_id = ''
        open_orders = self.demex_client.get_open_limit_orders()
        open_orders_list = list(open_orders.keys())
        while order_id in ['', '232570627D12F22489E4AC466DEEEFD56501645BB1F716998F688EB4EE95C081', 'F431BA8B17784DF8C2BAB72F704D703B32A52E96F261C105747EF0F3E872D27F']:
            order_id = open_orders_list[random.randint(a=0, b=len(open_orders_list)-1)]

        result: dict = self.demex_client.cancel_order(order_id=order_id)
        self.assertDictStructure(expect, result)

    def test_cancel_orders(self):
        expect: dict = {
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

        order_id_1 = ''
        order_id_2 = ''
        open_orders = self.demex_client.get_open_limit_orders()
        open_orders_list = list(open_orders.keys())
        while order_id_1 in ['', '232570627D12F22489E4AC466DEEEFD56501645BB1F716998F688EB4EE95C081', 'F431BA8B17784DF8C2BAB72F704D703B32A52E96F261C105747EF0F3E872D27F']:
            order_id_1 = open_orders_list[random.randint(a=0, b=len(open_orders_list)-1)]

        while order_id_2 in [order_id_1, '', '232570627D12F22489E4AC466DEEEFD56501645BB1F716998F688EB4EE95C081', 'F431BA8B17784DF8C2BAB72F704D703B32A52E96F261C105747EF0F3E872D27F']:
            order_id_2 = open_orders_list[random.randint(a=0, b=len(open_orders_list)-1)]

        order_ids = [order_id_1, order_id_2]

        result: dict = self.demex_client.cancel_orders(order_ids=order_ids)
        self.assertDictStructure(expect, result)

    # def test_get_open_limit_orders(self):
    #     self.demex_client.demex_client.get_open_limit_orders()
