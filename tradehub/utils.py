import base58
import binascii
import json
import math
import requests
from web3 import Web3


class TradehubApiException(Exception):

    def __init__(self, error_code, error_message, error):
        super(TradehubApiException, self).__init__(error_message)
        self.error_code = error_code
        self.error = error


class Request(object):

    def __init__(self, api_url='https://test-tradescan.switcheo.org', timeout=30):
        self.url = api_url.rstrip('/')
        self.timeout = timeout

    def get(self, path, params=None):
        """Perform GET request"""
        r = requests.get(url=self.url + path, params=params, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def post(self, path, data=None, json_data=None, params=None):
        """Perform POST request"""
        r = requests.post(url=self.url + path, data=data, json=json_data, params=params, timeout=self.timeout)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            raise TradehubApiException(r.json().get('error_code'), r.json().get('error_message'), r.json().get('error'))
        return r.json()

    def status(self):
        return self.get(path='/get_status')


def sort_and_stringify_json(message):
    """
    Return a JSON message that is alphabetically sorted by the key name
    Args:
        message
    """
    return json.dumps(message, sort_keys=True, separators=(',', ':'))


def to_tradehub_asset_amount(amount: float, decimals: int = 8):
    return "{:.0f}".format(amount * math.pow(10, decimals))


def reverse_hex(message: str):
    return "".join([message[x:x + 2] for x in range(0, len(message), 2)][::-1])


def is_valid_neo_public_address(address: str) -> bool:
    """Check if address is a valid NEO address"""
    valid = False

    if len(address) == 34 and address[0] == 'A':
        try:
            base58.b58decode_check(address.encode())
            valid = True
        except ValueError:
            # checksum mismatch
            valid = False

    return valid


def neo_get_scripthash_from_address(address: str):
    hash_bytes = binascii.hexlify(base58.b58decode_check(address))
    return reverse_hex(hash_bytes[2:].decode('utf-8'))


def is_eth_contract(address: str, web3_uri: str):
    eth_w3 = Web3(provider=Web3.HTTPProvider(endpoint_uri=web3_uri))
    if len(eth_w3.eth.get_code(eth_w3.toChecksumAddress(value=address))) == 0:
        return False
    else:
        return True


def format_withdraw_address(address: str, blockchain: str, web3_uri: str = None):
    if blockchain.lower() in ['neo'] and is_valid_neo_public_address(address=address):
        return reverse_hex(neo_get_scripthash_from_address(address=address))
    elif blockchain.lower() in ['eth', 'ethereum'] and Web3.isAddress(value=address):
        if is_eth_contract(address=address, web3_uri=web3_uri):
            raise ValueError('Cannot withdraw to an Ethereum contract address.')
        else:
            print("In Web3")
            return Web3.toChecksumAddress(value=address)[2:]
    else:
        raise ValueError('Not a valid address OR blockchain not yet supported.')
