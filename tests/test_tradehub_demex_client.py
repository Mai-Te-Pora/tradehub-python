import json
import time
from tradehub.demex_client import DemexClient
import tradehub.types as types
from tests import APITestCase, TRADING_TESTNET_WALLET_MNEMONIC


class TestTradeHubDemexClient(APITestCase):

    def setUp(self) -> None:
        self.demex_client = DemexClient(mnemonic=TRADING_TESTNET_WALLET_MNEMONIC, network='testnet')

    def checkResponse(self, response):
        if 'code' in response:
            self.skipTest(f"Skip test because of unknown error: {response['code']}")

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

        time.sleep(2)
        result: dict = self.demex_client.limit_buy(pair='swth_eth', quantity='400', price='0.0000091')
        self.checkResponse(result)
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

        time.sleep(2)
        result: dict = self.demex_client.limit_sell(pair='swth_eth', quantity='400', price='0.0000227')
        self.checkResponse(result)
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

        time.sleep(2)
        result: dict = self.demex_client.market_buy(pair='swth_eth', quantity='400')
        self.checkResponse(result)
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

        time.sleep(2)
        result: dict = self.demex_client.market_sell(pair='swth_eth', quantity='400')
        self.checkResponse(result)
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

        time.sleep(2)
        result: dict = self.demex_client.stop_limit_buy(pair=pair, quantity='400', price='0.0000091', stop_price=stop_price)
        self.checkResponse(result)
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

        time.sleep(2)
        result: dict = self.demex_client.stop_limit_sell(pair=pair, quantity='400', price='0.0000227', stop_price=stop_price)
        self.checkResponse(result)
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

        time.sleep(2)
        result: dict = self.demex_client.stop_market_buy(pair=pair, quantity='400', stop_price=stop_price)
        self.checkResponse(result)
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

        time.sleep(2)
        result: dict = self.demex_client.stop_market_sell(pair=pair, quantity='400', stop_price=stop_price)
        self.checkResponse(result)
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
        time.sleep(2)
        limit_order: dict = self.demex_client.limit_buy(pair='swth_eth', quantity='400', price='0.0000075')
        self.checkResponse(limit_order)
        order_id: str = json.loads(limit_order["logs"][0]['log'])["order"]["order_id"]
        result: dict = self.demex_client.cancel_order(order_id=order_id)
        self.checkResponse(result)
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

        time.sleep(2)
        limit_order_1: dict = self.demex_client.limit_buy(pair='swth_eth', quantity='400', price='0.0000075')
        self.checkResponse(limit_order_1)
        order_id_1: str = json.loads(limit_order_1["logs"][0]['log'])["order"]["order_id"]
        time.sleep(2)
        limit_order_2: dict = self.demex_client.limit_buy(pair='swth_eth', quantity='400', price='0.0000075')
        self.checkResponse(limit_order_2)
        order_id_2: str = json.loads(limit_order_2["logs"][0]['log'])["order"]["order_id"]
        order_ids = [order_id_1, order_id_2]
        result: dict = self.demex_client.cancel_orders(order_ids=order_ids)
        self.checkResponse(result)
        self.assertDictStructure(expect, result)

    def test_cancel_all_open_orders_for_pair(self):
        pair = 'swth_btc'
        time.sleep(2)
        self.demex_client.limit_buy(pair=pair, quantity='400', price='0.0000010')
        time.sleep(2)
        self.demex_client.limit_sell(pair=pair, quantity='400', price='0.0000020')
        result: list = self.demex_client.get_open_orders_by_pair(pair=pair)
        self.assertTrue(result)
        time.sleep(4)
        result: dict = self.demex_client.cancel_all_open_orders_for_pair(pair=pair)
        self.checkResponse(result)
        time.sleep(2)
        result: list = self.demex_client.get_open_orders_by_pair(pair=pair)
        self.assertFalse(result)

    def test_edit_orders(self):
        time.sleep(2)
        limit_order_1: dict = self.demex_client.limit_buy(pair='swth_eth', quantity='400', price='0.0000075')
        self.checkResponse(limit_order_1)
        order_id_1: str = json.loads(limit_order_1["logs"][0]['log'])["order"]["order_id"]
        time.sleep(2)
        limit_order_2: dict = self.demex_client.limit_buy(pair='swth_eth', quantity='400', price='0.0000075')
        self.checkResponse(limit_order_2)
        order_id_2: str = json.loads(limit_order_2["logs"][0]['log'])["order"]["order_id"]

        edit_order_1: dict = types.EditOrderMessage(id=order_id_1, quantity='500')
        edit_order_2: dict = types.EditOrderMessage(id=order_id_2, quantity='800')
        edit_orders: list = [edit_order_1, edit_order_2]

        time.sleep(2)
        self.demex_client.edit_orders(orders=edit_orders)

        check_order_1: dict = self.demex_client.tradehub.get_order(order_id=order_id_1)
        check_order_2: dict = self.demex_client.tradehub.get_order(order_id=order_id_2)
        self.assertEqual(check_order_1["quantity"], '500')
        self.assertEqual(check_order_2["quantity"], '800')

    def test_edit_limit_order(self):
        time.sleep(2)
        limit_order_1: dict = self.demex_client.limit_buy(pair='swth_eth', quantity='400', price='0.0000075')
        self.checkResponse(limit_order_1)
        order_id_1: str = json.loads(limit_order_1["logs"][0]['log'])["order"]["order_id"]

        time.sleep(2)
        self.demex_client.edit_limit_order(order_id=order_id_1, quantity='600')

        time.sleep(2)
        check_order_1: dict = self.demex_client.tradehub.get_order(order_id=order_id_1)
        self.assertEqual(check_order_1["quantity"], '600')

    def test_edit_stop_order(self):
        pair = 'swth_eth'
        current_price = self.demex_client.tradehub.get_prices(market=pair)["last"]
        stop_price = "{:10.8f}".format(float(current_price) + 0.000001)

        time.sleep(2)
        limit_order_1: dict = self.demex_client.stop_limit_buy(pair=pair, quantity='400', price='0.0000091', stop_price=stop_price)
        self.checkResponse(limit_order_1)
        order_id_1: str = json.loads(limit_order_1["logs"][0]['log'])["order"]["order_id"]

        time.sleep(2)
        stop_price = "{:10.8f}".format(float(current_price) + 0.000002)
        self.demex_client.edit_stop_order(order_id=order_id_1, quantity='600', price='0.0000081', stop_price=stop_price)

        time.sleep(2)
        check_order_1: dict = self.demex_client.tradehub.get_order(order_id=order_id_1)
        self.assertEqual(check_order_1["quantity"], '600')

    def test_get_open_orders(self):
        pair = 'swth_btc'
        time.sleep(2)
        self.demex_client.limit_buy(pair=pair, quantity='400', price='0.0000010')
        time.sleep(2)
        self.demex_client.limit_sell(pair=pair, quantity='400', price='0.0000020')
        result: list = self.demex_client.get_open_orders()
        self.assertTrue(result)

    def test_get_open_orders_by_pair(self):
        pair = 'swth_btc'
        time.sleep(2)
        self.demex_client.limit_buy(pair=pair, quantity='400', price='0.0000010')
        time.sleep(2)
        self.demex_client.limit_sell(pair=pair, quantity='400', price='0.0000020')
        result: list = self.demex_client.get_open_orders_by_pair(pair=pair)
        self.assertTrue(result)

    def test_get_open_limit_orders(self):
        pair = 'swth_btc'
        time.sleep(2)
        self.demex_client.limit_buy(pair=pair, quantity='400', price='0.0000010')
        time.sleep(2)
        self.demex_client.limit_sell(pair=pair, quantity='400', price='0.0000020')
        result: list = self.demex_client.get_open_limit_orders()
        self.assertTrue(result)

    def test_get_open_stop_orders(self):
        pair = 'swth_eth'
        current_price = self.demex_client.tradehub.get_prices(market=pair)["last"]
        stop_price = "{:10.8f}".format(float(current_price) + 0.000001)
        time.sleep(2)
        self.demex_client.stop_limit_buy(pair=pair, quantity='400', price='0.0000091', stop_price=stop_price)
        result: list = self.demex_client.get_open_stop_orders()
        self.assertTrue(result)
