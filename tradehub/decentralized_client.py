"""
Description:

    Decentralized Client Class for Crawling the Tradehub network.
    This client is the basis to all classes because it allows network calls to fail over to other nodes.
    This class is designed to find available public nodes to interact with for API and Websocket calls.

Usage::

    from tradehub.decentralized_client import NetworkCrawlerClient
"""

import multiprocessing as mp
from tradehub.utils import Request
import random
from requests.exceptions import ConnectionError, HTTPError, Timeout
import socket
# import threading


class NetworkCrawlerClient(object):
    """
    This class crawls the Switcheo Validator network to build a list of accessible endpoints for APIs and Websockets.
    Execution of this function is as follows::

        NetworkCrawlerClient(network='mainnet',
                             trusted_ip_list=None,
                             trusted_uri_list=None,
                             is_secure=False,
                             is_websocket_client=True)
    """

    def __init__(self,
                 network: str = "testnet",
                 trusted_ip_list: list = None,
                 trusted_uri_list: list = None,
                 is_secure: bool = False,
                 is_websocket_client: bool = False):
        """
        :param network: The network you want to interact with. Accepts "testnet" or "mainnet".
        :type network: str
        :param trusted_ip_list: Known and trusted IPs to connect to for your API requests.
        :type trusted_ip_list: list
        :param trusted_uri_list: Known and trusted URIs to connect to for your API requests.
        :type trusted_uri_list: list
        :param is_secure: Flag for setting secure connection on or off.
        :type is_secure: bool
        :param is_websocket_client: Flag for finding and setting websocket variables.
        :type is_websocket_client: bool
        """
        if network.lower() not in ["main", "mainnet", "test", "testnet"]:
            raise ValueError("Parameter network - {} - is not valid, requires main, mainnent, test, or testnet.".format(network))

        if trusted_ip_list and trusted_uri_list:
            raise ValueError("Can't use both IP and URI list, only pass one option.")

        if trusted_ip_list or trusted_uri_list:
            self.BYPASS_NETWORK_CRAWLER = True
        else:
            self.BYPASS_NETWORK_CRAWLER = False

        self.is_secure = is_secure
        if self.is_secure:
            self.http_string = 'https'
            self.ws_string = 'wss'
        else:
            self.http_string = 'http'
            self.ws_string = 'ws'
        self.is_websocket_client = is_websocket_client
        self.active_ws_uri_list = []

        if not self.BYPASS_NETWORK_CRAWLER:
            self.seed_peers_list = {
                "main": ["54.255.5.46", "175.41.151.35"],
                "mainnet": ["54.255.5.46", "175.41.151.35"],
                "test": ["54.255.42.175", "52.220.152.108"],
                "testnet": ["54.255.42.175", "52.220.152.108"],
            }
            self.tradescan_node_url = {
                "main": "https://switcheo.org/nodes?net=main",
                "mainnet": "https://switcheo.org/nodes?net=main",
                "test": "https://switcheo.org/nodes?net=test",
                "testnet": "https://switcheo.org/nodes?net=test",
            }

            self.all_peers_list = self.seed_peers_list[network.lower()]
            self.active_validator_list = []
            self.active_sentry_api_list = []
            self.validator_crawler_mp()
            self.sentry_status_request(uri=False)
        elif trusted_ip_list:
            self.all_peers_list = trusted_ip_list
            self.active_validator_list = trusted_ip_list
            self.active_sentry_api_list = []
            self.sentry_status_request(uri=False)
        elif trusted_uri_list:
            self.all_peers_list = trusted_uri_list
            self.active_validator_list = trusted_uri_list
            self.active_sentry_api_list = []
            self.sentry_status_request(uri=True)
        self.active_sentry_uri = self.active_sentry_api_list[random.randint(a=0, b=len(self.active_sentry_api_list)-1)]
        self.active_sentry_api_ip = self.active_sentry_uri.split(':')[1][2:]
        if self.is_websocket_client:
            self.active_ws_uri = self.active_ws_uri_list[random.randint(a=0, b=len(self.active_ws_uri_list)-1)]
            self.active_ws_ip = self.active_ws_uri.split(':')[1][2:]

    def validator_crawler_mp(self):
        """
        Crawl the Tradehub Validators to test for available API endpoints.

        Execution of this function is as follows::

            validator_crawler_mp()
        """
        checked_peers_list = []
        unchecked_peers_list = list(set(self.all_peers_list) - set(checked_peers_list))

        while unchecked_peers_list:

            pool = mp.Pool(processes=10)
            validator_outputs = pool.map(self.validator_status_request, unchecked_peers_list)
            pool.close()
            pool.join()

            for validator in validator_outputs:
                self.all_peers_list.append(validator["ip"])
                checked_peers_list.append(validator["ip"])
                if validator["validator_status"] == "Active" and not validator["catching_up"]:
                    self.active_validator_list.append(validator["ip"])
                for connected_node in validator["connected_nodes"]:
                    self.all_peers_list.append(connected_node["node_ip"])

            self.all_peers_list = list(dict.fromkeys(self.all_peers_list))
            checked_peers_list = list(dict.fromkeys(checked_peers_list))
            self.active_validator_list = list(dict.fromkeys(self.active_validator_list))
            unchecked_peers_list = list(set(self.all_peers_list) - set(checked_peers_list))

            # If the initial peers do not return any reults, query Tradescan API.
            # if not self.active_peers_list:
            #     validators = Request(api_url=self.tradescan_node_url, timeout=30).get()
            #     for validator in validators:
            #         unchecked_peers_list.append(validator["ip"])

    def validator_status_request(self, validator_ip: str):
        """
        Function that makes the network requests to the Tradehub validators across the network.

        Execution of this function is as follows::

            validator_status_request(validator_ip='54.255.5.46')

        The expected return result for this function is as follows::

            {
                'moniker': 'spock',
                'id': 'ca1189045e84d2be5db0a1ed326ce7cd56015f11',
                'ip': '54.255.5.46',
                'version': '0.33.7',
                'network': 'switcheo-tradehub-1',
                'latest_block_hash': 'DF194D43058D3CD89DD98A7DA28164B239B9693C822A1DB16CCC27FB49CA587B',
                'latest_block_height': '7995864',
                'latest_block_time': '2021-02-27T19:51:00.162091183Z',
                'earliest_block_height': '1',
                'earliest_block_time': '2020-08-14T07:32:27.856700491Z',
                'catching_up': False,
                'validator_address': '7091A72888509B3F3069231081621DC988D63542',
                'validator_pub_key_type': 'tendermint/PubKeyEd25519',
                'validator_pub_key': 'epMp0h65WflL7r8tPGQwusVMbCHgy7ucRg8eDlEJPW0=',
                'validator_voting_power': '0',
                'validator_status': 'Active',
                'connected_nodes': [
                    {
                        'node_id': 'd57a64f41487b5e421e91b71dceb0784cae57733',
                        'node_ip': '195.201.82.228',
                        'node_full': 'd57a64f41487b5e421e91b71dceb0784cae57733@195.201.82.228'
                    },
                    ...
                ]
            }

        :param validator_ip: String of the IP address to connect to.
        :return: Dictionary of validators that the crawler has found with the status.
        """
        validator_status = {}
        try:
            process_peer = True
            validator_status["ip"] = validator_ip
            i = Request(api_url="{}://{}:26657".format(self.http_string, validator_ip), timeout=1).get(path='/net_info')
        except (ValueError, ConnectionError, HTTPError, Timeout) as e:
            validator_status["validator_status"] = "Unknown - Cannot Connect to Retrieve Validator INFO - {}".format(e)
            validator_status["connected_nodes"] = []
            process_peer = False

        if process_peer:
            connected_nodes = []

            for connected_peer in i["result"]["peers"]:
                connected_nodes.append({
                    "node_id": connected_peer["node_info"]["id"],
                    "node_ip": connected_peer["remote_ip"],
                    "node_full": "{}@{}".format(connected_peer["node_info"]["id"], connected_peer["remote_ip"])
                })

            try:
                s = Request(api_url="{}://{}:26657".format(self.http_string, validator_ip), timeout=1).get(path='/status')
            except (ValueError, ConnectionError, HTTPError, Timeout) as e:
                validator_status["validator_status"] = "Unknown - Cannot Connect to Retrieve Status end point - {}".format(e)
                validator_status["connected_nodes"] = []
                process_peer = False

            if process_peer:
                validator_status = self.parse_validator_status(request_json=s, validator_ip=validator_ip)
                validator_status["validator_status"] = "Active"
                validator_status["connected_nodes"] = connected_nodes

        return validator_status

    def parse_validator_status(self, request_json: dict, validator_ip: str):
        """
        Function to parse each peer's JSON element and build information about each.

        Execution of this function is as follows::

            parse_validator_status(request_json='/status', validator_ip='54.255.5.46')

        The expected return result for this function is as follows::

            {
                'moniker': 'spock',
                'id': 'ca1189045e84d2be5db0a1ed326ce7cd56015f11',
                'ip': '54.255.5.46',
                'version': '0.33.7',
                'network': 'switcheo-tradehub-1',
                'latest_block_hash': 'DF194D43058D3CD89DD98A7DA28164B239B9693C822A1DB16CCC27FB49CA587B',
                'latest_block_height': '7995864',
                'latest_block_time': '2021-02-27T19:51:00.162091183Z',
                'earliest_block_height': '1',
                'earliest_block_time': '2020-08-14T07:32:27.856700491Z',
                'catching_up': False,
                'validator_address': '7091A72888509B3F3069231081621DC988D63542',
                'validator_pub_key_type': 'tendermint/PubKeyEd25519',
                'validator_pub_key': 'epMp0h65WflL7r8tPGQwusVMbCHgy7ucRg8eDlEJPW0=',
                'validator_voting_power': '0'
            }

        :param request_json: Dictionary of the return response from the validator status request.
        :param validator_ip: String of the IP address to connect to.
        :return: Dictionary of validator information.
        """
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

    def sentry_status_request(self, uri: bool = False):
        """
        This function is here to ensure the nodes that have open network connections also have their persistence service running.
        Many times the network connection is open for communication but the persistence service will not be on.

        Execution of this function is as follows::

            sentry_status_request(uri=True)

        :param uri: Bool value for a URI or IP address.
        """
        for active_validator in self.active_validator_list:
            if uri:
                try:
                    # Have to check the "/get_status" endpoint because the port could be open and the validator fully synced but have the persistence service inactive, shutdown, stopped, or non-repsonsive.
                    Request(api_url=active_validator, timeout=1).get(path='/get_status')
                    self.active_sentry_api_list.append(active_validator)
                    if self.is_websocket_client:
                        self.websocket_status_check(ip=active_validator)
                except (ValueError, ConnectionError, HTTPError, Timeout):
                    pass
            else:
                # 1318 - Cosmos REST; 5001 - Demex REST; 5002 - Reverse Proxy for Demex and Cosmos REST; Recommended to not use proxy
                for port in ["5001"]:
                    try:
                        # Have to check the "/get_status" endpoint because the port could be open and the validator fully synced but have the persistence service inactive, shutdown, stopped, or non-repsonsive.
                        Request(api_url="{}://{}:{}".format(self.http_string, active_validator, port), timeout=1).get(path='/get_status')
                        self.active_sentry_api_list.append('{}://{}:{}'.format(self.http_string, active_validator, port))
                        if self.is_websocket_client:
                            self.websocket_status_check(ip=active_validator)
                    except (ValueError, ConnectionError, HTTPError, Timeout):
                        pass

        self.active_sentry_api_list = list(dict.fromkeys(self.active_sentry_api_list))
        self.active_ws_uri_list = list(dict.fromkeys(self.active_ws_uri_list))

    def websocket_status_check(self, ip: str, port: int = 5000):
        """
        Function to check if the websocket port is open for communication.
        This is called as part of the sentry check because calling the websocket also requires the persistence service to be available.

        Execution of this function is as follows::

            websocket_status_check(ip='54.255.5.46', port=5000)

        :param ip: String of the IP address to connect to.
        :param port: Int value for the port to be checked.
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            location = (ip, port)
            result_of_check = s.connect_ex(location)
            if result_of_check == 0:
                self.active_ws_uri_list.append('{}://{}:{}/ws'.format(self.ws_string, ip, port))
            s.close()
        except socket.error:
            pass

    # def update_validators_and_sentries(self):
    #     threading.Timer(5.0, self.update_validators_and_sentries).start()
    #     self.validator_crawler_mp()
    #     self.sentry_status_request()
    #     self.active_sentry_api_ip = self.active_sentry_api_list[random.randint(a=0, b=len(self.active_sentry_api_list)-1)]

    def tradehub_get_request(self, path: str, params: dict = None):
        """
        This is a wrapper for the get request function to allow for retrying network calls on different available validators if a request fails.

        Execution of this function is as follows::

            tradehub_get_request(path='/txs')

        :param path: String of the path being used for the network request that is going to be made.
        :param params: Dict values that will added to the get request.
        :return: Dictionary of the return request based on the network path sent.
        """
        try:
            req = Request(api_url=self.active_sentry_uri, timeout=2).get(path=path, params=params)
            return req
        except (ValueError, ConnectionError, HTTPError, Timeout):
            self.active_sentry_api_list.remove(self.active_sentry_uri)
            if not self.active_sentry_api_list and not self.BYPASS_NETWORK_CRAWLER:
                self.validator_crawler_mp()
                self.sentry_status_request()
            elif not self.active_sentry_api_list and self.BYPASS_NETWORK_CRAWLER:
                raise ValueError("Provided Sentry API IP addresses are not responding.")
            self.active_sentry_uri = self.active_sentry_api_list[random.randint(a=0, b=len(self.active_sentry_api_list)-1)]
            return self.tradehub_get_request(path=path, params=params)

    def tradehub_post_request(self, path: str, data: dict = None, json_data: dict = None, params: dict = None):
        """
        This is a wrapper for the post request function to allow for retrying network calls on different available validators if a request fails.

        Execution of this function is as follows::

            tradehub_post_request(path='/txs')

        :param path: String of the path being used for the network request that is going to be made.
        :param data: Dict values that will added to the post request.
        :param json_data: Dict values that will added to the post request.
        :param params: Dict values that will added to the post request.
        :return: Dictionary of the return request based on the network path sent.
        """
        try:
            req = Request(api_url=self.active_sentry_uri, timeout=2).post(path=path, data=data, json_data=json_data, params=params)
            return req
        except (ValueError, ConnectionError, HTTPError, Timeout):
            self.active_sentry_api_list.remove(self.active_sentry_uri)
            if not self.active_sentry_api_list and not self.BYPASS_NETWORK_CRAWLER:
                self.validator_crawler_mp()
                self.sentry_status_request()
            elif not self.active_sentry_api_list and self.BYPASS_NETWORK_CRAWLER:
                raise ValueError("Provided Sentry API IP addresses are not responding.")
            self.active_sentry_uri = self.active_sentry_api_list[random.randint(a=0, b=len(self.active_sentry_api_list)-1)]
            return self.tradehub_post_request(path=path, data=data, json_data=json_data, params=params)
