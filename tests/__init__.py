import os
from unittest import TestCase

from tradehub.public_client import PublicClient

mainnet_client = PublicClient(network='mainnet', is_websocket_client=True)
MAINNET_VAL_IP = mainnet_client.active_sentry_api_ip
MAINNET_WS_URI = mainnet_client.active_ws_uri
testnet_client = PublicClient(network='testnet', is_websocket_client=True)
TESTNET_VAL_IP = testnet_client.active_sentry_api_ip
TESTNET_WS_URI = testnet_client.active_ws_uri

WALLET_VALIDATOR = "swth1vwges9p847l9csj8ehrlgzajhmt4fcq4sd7gzl"
WALLET_DEVEL = "swth1qlue2pat9cxx2s5xqrv0ashs475n9va963h4hz"
WALLET_SWTH_ETH1_AMM = "swth1p5hjhag5glkpqaj0y0vn3au7x0vz33k0gxuejk"
USERNAME_DEVEL = "devel484"

WALLET_MNEMONIC = "refuse flag merge fiction choose dream frown gauge need fabric once pizza actual armed reopen couple family fury reopen slush blue try focus minute"
WALLET_PRIVATE_KEY = b'\x15\xcf\xdd\xdf\xead\x88\xd2y!\xdb\xb61\xa6\x98\xeeQm\x05\xed\x8d%43!\n\xccS\xcbsf\x90'
WALLET_PUBLIC_KEY = b'\x02o\x1f\xfbL\x96\xe8\x1e\xb0\x12V\x80\xc7t\xfc\xb40R\xaeu\xf3{\xf6\xd7m]\xd1\xa9\x91\xa8\xe0Df'
WALLET_ADDRESS = 'tswth1upcgussnx4p3jegwj3x2fccwlajwckkzgstrp8'

TRADING_TESTNET_WALLET_MNEMONIC = "venture consider cool fury front middle junk person suit assist garbage category"

NEO_ADDRESS = 'APuP9GsSCPJKrexPe49afDV8CQYubZGWd8'
NEO_CONTRACT = '3e09e602eeeb401a2fec8e8ea137d59aae54a139'
ETH_ADDRESS = '0x32c46323b51c977814e05ef5e258ee4da0e4c3c3'   # Ropsten Testnet Address
ETH_CONTRACT = '0x0025b3342582d106454e88ecb091f3e456f81ac3'  # Sushi Ropsten Testnet Contract

WEB3_API_KEY = os.environ.get('WEB3_API_KEY')
WEB3_API_URL = 'https://eth-ropsten.alchemyapi.io/v2/{}'.format(WEB3_API_KEY)

WEBSOCKET_TIMEOUT_GET_REQUEST = 5
WEBSOCKET_TIMEOUT_SUBSCRIPTION = 60


class APITestCase(TestCase):

    def assertDictStructure(self, expect: dict, actual: dict, path: list = []) -> None:
        """
        Compare function to check if expected dict with types equals the actual dict. If a dict has a dict as field
        the function call it self recursive.

        :raise AssertionError: if actual type and expected types are not same
        :raise AssertionError: if keys in actual and expected are not same

        :param expect: dict with types
        :param actual: dict with values
        :param path: current path(list with keys)
        :return: None
        """
        self.assertEqual(expect.keys(), actual.keys(),
                         msg=f"Expected field keys are not same: {self.path_to_dict_path(path)}")
        for key in actual:
            if isinstance(expect[key], dict):
                self.assertIsInstance(actual[key], dict,
                                      msg=f"Expected field {self.path_to_dict_path(path+[key])} to be type dict, "
                                          f"got type {type(actual[key])} instead")
                self.assertDictStructure(expect[key], actual[key], path + [key])
            elif isinstance(expect[key], list):
                self.assertIsInstance(actual[key], list,
                                      msg=f"Expected field {self.path_to_dict_path(path+[key])} to be type list, "
                                          f"got type {type(actual[key])} instead")

                if not expect[key]:
                    self.assertFalse(actual[key], msg=f"Expected empty list {self.path_to_dict_path(path+[key])},"
                                                      f"received non empty list {actual[key]}")
                else:
                    self.assertTrue(actual[key], msg=f"Expected list {self.path_to_dict_path(path+[key])},"
                                                     f"received empty list {actual[key]}")

                if expect[key] and isinstance(expect[key][0], dict):
                    for i, entry in enumerate(actual[key]):
                        self.assertDictStructure(expect[key][0], entry, path + [key, i])
                else:
                    for i, entry in enumerate(actual[key]):
                        self.assertIsInstance(entry, expect[key][0],
                                              msg=f"Expected field {self.path_to_dict_path(path+[key, i])} "
                                                  f"to be type {expect[key][0]}, got type {type(entry)} instead")
            else:
                if type(expect[key]) == type:
                    self.assertIsInstance(actual[key], expect[key],
                                          msg=f"Expected field {self.path_to_dict_path(path+[key])} "
                                              f"to be type {expect[key]}, got type {type(actual[key])} instead")
                else:
                    self.assertIn(type(actual[key]), expect[key].__args__,
                                  msg=f"Expected field {self.path_to_dict_path(path+[key])} "
                                      f"to be type {expect[key]}, got type {type(actual[key])} instead")

    @staticmethod
    def path_to_dict_path(path: list) -> str:
        """
        This method returns the dict path to a field.

        path_to_dict_path(["layer1", "layer2, "key"])
        -> "['layer1']['layer2']['key']"

        :param path: list with keys(path)
        :return: dict path as str
        """
        return "".join([f"['{key}']" for key in path])
