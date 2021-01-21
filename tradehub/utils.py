import base58
import binascii
import json
import math
import multiprocessing as mp
import requests
from web3 import Web3


class TradehubApiException(Exception):

    def __init__(self, error_code, error_message, error):
        super(TradehubApiException, self).__init__(error_message)
        self.error_code = error_code
        self.error = error

class Request(object):

    def __init__(self, api_url = 'https://switcheo.org', timeout = 30):
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
        r = requests.get(url=self.url)
        r.raise_for_status()
        return r.json()

def sort_and_stringify_json(message):
    """
    Return a JSON message that is alphabetically sorted by the key name
    Args:
        message
    """
    return json.dumps(message, sort_keys=True, separators=(',', ':'))

# def validator_crawler(network = 'test'):
#     peers_dict = {}
#     all_peers_list = []
#     checked_peers_list = []
#     active_peers_list = []
#     continue_checking_peers = True
#     seed_peers_list = {
#         "main": ["54.255.5.46", "168.119.70.59", "192.99.247.238", "40.87.48.237", "18.141.90.114"],
#         "test": ["54.255.42.175", "52.220.152.108"]
#     }

#     if network in ["main", "test"]:
#         all_peers_list = seed_peers_list[network]

#     while continue_checking_peers:
#         unchecked_peers_list = list(set(all_peers_list) - set(checked_peers_list))
#         print("Unchecked Peers: {}".format(unchecked_peers_list))
#         for peer in unchecked_peers_list:
#             print(peer)
#             try:
#                 process_peer = True
#                 i = requests.get("http://{}:26657/net_info".format(peer), timeout=1)
#             except requests.exceptions.Timeout:
#                 print("{} timed out on net_info.".format(peer))
#                 peers_dict[peer] = {
#                     "validator_status": "Unknown - Cannot Connect to Retrieve Validator INFO",
#                     "connected_nodes": []
#                 }
#                 process_peer = False
#             except requests.exceptions.ConnectionError:
#                 print("{} Connection Error; max retries exceeded with url: net_info.".format(peer))
#                 peers_dict[peer] = {
#                     "validator_status": "Unknown - Cannot Connect to Retrieve Validator INFO",
#                     "connected_nodes": []
#                 }
#                 process_peer = False

#             all_peers_list.append(peer)
#             checked_peers_list.append(peer)
#             if i.status_code == 200 and process_peer:
#                 connected_nodes = []

#                 for connected_peer in i.json()["result"]["peers"]:
#                     all_peers_list.append(connected_peer["remote_ip"])
#                     connected_nodes.append({
#                         "node_id": connected_peer["node_info"]["id"],
#                         "node_ip": connected_peer["remote_ip"],
#                         "node_full": "{}@{}".format(connected_peer["node_info"]["id"], connected_peer["remote_ip"])
#                     })
                
#                 try:
#                     s = requests.get("http://{}:26657/status".format(peer))
#                 except requests.exceptions.Timeout:
#                     print("{} timed out on status.".format(peer))
#                     peers_dict[peer] = {
#                         "validator_status": "Unknown - Cannot Connect to Retrieve Status end point",
#                         "connected_nodes": []
#                     }
#                     process_peer = False
#                 except requests.exceptions.ConnectionError:
#                     print("{} Connection Error; max retries exceeded with url: status.".format(peer))
#                     peers_dict[peer] = {
#                         "validator_status": "Unknown - Cannot Connect to Retrieve Status end point",
#                         "connected_nodes": []
#                     }
#                     process_peer = False
                
#                 if s.status_code == 200 and process_peer:
#                     peers_dict[peer] = parse_validator_status(request_json = s.json())
#                     peers_dict["validator_status"] = "Active"
#                     peers_dict["connected_nodes"] = connected_nodes
#                     if not peers_dict[peer]["catching_up"]:
#                         active_peers_list.append(peer)
                
#                 all_peers_list = list(dict.fromkeys(all_peers_list))
#                 checked_peers_list = list(dict.fromkeys(checked_peers_list))
#                 active_peers_list = list(dict.fromkeys(active_peers_list))
        
#         unchecked_peers_list = list(set(all_peers_list) - set(checked_peers_list))
#         print("Unchecked Peers: {}".format(unchecked_peers_list))
#         if not unchecked_peers_list and active_peers_list:
#             continue_checking_peers = False
#         elif not unchecked_peers_list and not active_peers_list:
#             validators = Request(api_url = 'https://tradescan.switcheo.org', timeout = 30).get(path = '/monitor')
#             for validator in validators:
#                 unchecked_peers_list.append(validator["ip"])
    
#     peers_dict["active_peers"] = active_peers_list
#     # print(peers_dict)
#     # print(peers_dict["active_peers"])


def validator_crawler_mp(network = 'test'):
    peers_dict = {}
    all_peers_list = []
    checked_peers_list = []
    active_peers_list = []
    continue_checking_peers = True

    seed_peers_list = {
        "main": ["54.255.5.46", "175.41.151.35"],
        "test": ["54.255.42.175", "52.220.152.108"]
    }

    if network in ["main", "test"]:
        all_peers_list = seed_peers_list[network]

    while continue_checking_peers:
        unchecked_peers_list = list(set(all_peers_list) - set(checked_peers_list))

        pool = mp.Pool(processes = 10)
        validator_outputs = pool.map(validator_status_request, unchecked_peers_list)
        pool.close()
        pool.join()

        for validator in validator_outputs:
            all_peers_list.append(validator["ip"])
            checked_peers_list.append(validator["ip"])
            if validator["validator_status"] == "Active" and not validator["catching_up"]:
                active_peers_list.append(validator["ip"])
            for connected_node in validator["connected_nodes"]:
                all_peers_list.append(connected_node["node_ip"])
            
        all_peers_list = list(dict.fromkeys(all_peers_list))
        checked_peers_list = list(dict.fromkeys(checked_peers_list))
        active_peers_list = list(dict.fromkeys(active_peers_list))
        unchecked_peers_list = list(set(all_peers_list) - set(checked_peers_list))

        if not unchecked_peers_list and active_peers_list:
            continue_checking_peers = False
        elif not unchecked_peers_list and not active_peers_list:
            validators = Request(api_url = 'https://tradescan.switcheo.org', timeout = 30).get(path = '/monitor')
            for validator in validators:
                unchecked_peers_list.append(validator["ip"])
    
    peers_dict["active_peers"] = active_peers_list
    return peers_dict

def validator_status_request(validator_ip):
    validator_status = {}
    try:
        process_peer = True
        validator_status["ip"] = validator_ip
        i = requests.get("http://{}:26657/net_info".format(validator_ip), timeout=1)
    except requests.exceptions.Timeout:
        validator_status["validator_status"] = "Unknown - Cannot Connect to Retrieve Validator INFO"
        validator_status["connected_nodes"] = []
        process_peer = False
    except requests.exceptions.ConnectionError:
        validator_status["validator_status"] = "Unknown - Cannot Connect to Retrieve Validator INFO"
        validator_status["connected_nodes"] = []
        process_peer = False
    
    if process_peer and i.status_code == 200:
        connected_nodes = []

        for connected_peer in i.json()["result"]["peers"]:
            connected_nodes.append({
                "node_id": connected_peer["node_info"]["id"],
                "node_ip": connected_peer["remote_ip"],
                "node_full": "{}@{}".format(connected_peer["node_info"]["id"], connected_peer["remote_ip"])
            })
                
        try:
            s = requests.get("http://{}:26657/status".format(validator_ip))
        except requests.exceptions.Timeout:
            validator_status["validator_status"] = "Unknown - Cannot Connect to Retrieve Status end point"
            validator_status["connected_nodes"] = []
            process_peer = False
        except requests.exceptions.ConnectionError:
            validator_status["validator_status"] = "Unknown - Cannot Connect to Retrieve Status end point"
            validator_status["connected_nodes"] = []
            process_peer = False
                
        if process_peer and s.status_code == 200:
            validator_status = parse_validator_status(request_json = s.json(), validator_ip = validator_ip)
            validator_status["validator_status"] = "Active"
            validator_status["connected_nodes"] = connected_nodes
        elif process_peer and s.status_code != 200:
            validator_status["validator_status"] = "Disabled - Status Endpoint - Status code {} received".format(i.status_code)
            validator_status["connected_nodes"] = []
            process_peer = False
    
    elif process_peer and i.status_code != 200:
        validator_status["validator_status"] = "Disabled - Net Info Endpoint - Status code {} received".format(i.status_code)
        validator_status["connected_nodes"] = []
        process_peer = False
    
    return validator_status

def parse_validator_status(request_json, validator_ip):
    return {
        "moniker": request_json["result"]["node_info"]["moniker"],
        "id": request_json["result"]["node_info"]["id"],
        "ip": validator_ip,
        "version": request_json["result"]["node_info"]["version"],
        "network": request_json["result"]["node_info"]["network"],
        "latest_block_hash": request_json["result"]["sync_info"]["latest_block_hash"],
        "latest_block_height": request_json["result"]["sync_info"]["latest_block_height"],
        "latest_block_time": request_json["result"]["sync_info"]["latest_block_time"],
        "earliest_block_height": request_json["result"]["sync_info"]["earliest_block_height"],
        "earliest_block_time": request_json["result"]["sync_info"]["earliest_block_time"],
        "catching_up": request_json["result"]["sync_info"]["catching_up"],
        "validator_address": request_json["result"]["validator_info"]["address"],
        "validator_pub_key_type": request_json["result"]["validator_info"]["pub_key"]["type"],
        "validator_pub_key": request_json["result"]["validator_info"]["pub_key"]["value"],
        "validator_voting_power": request_json["result"]["validator_info"]["voting_power"]
    }

def to_tradehub_asset_amount(amount: float, decimals: int = 8):
    return "{:.0f}".format(amount * math.pow(10, decimals))

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

def reverse_hex(message: str):
    return "".join([message[x:x + 2] for x in range(0, len(message), 2)][::-1])

def neo_get_scripthash_from_address(address: str):
    hash_bytes = binascii.hexlify(base58.b58decode_check(address))
    return reverse_hex(hash_bytes[2:].decode('utf-8'))

def is_eth_contract(address: str, web3_uri: str):
    eth_w3 = Web3(provider = Web3.HTTPProvider(endpoint_uri = web3_uri))
    if len(eth_w3.eth.getCode(eth_w3.toChecksumAddress(value = address))) == 0:
        return True
    else:
        return False

def format_withdraw_address(address: str):
    if is_valid_neo_public_address(address = address):
        return reverse_hex(neo_get_scripthash_from_address(address = address))
    elif Web3.isAddress(value = address):
        if is_eth_contract(address = address):
            raise ValueError('Cannot withdraw to an Ethereum contract address.')
        else:
            return Web3.toChecksumAddress(value = address)[2:]
    else:
        raise ValueError('Not a valid address or blockchain not yet supported.')
