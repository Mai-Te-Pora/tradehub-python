import multiprocessing as mp
from tradehub.utils import Request
import random
from requests.exceptions import ConnectionError, HTTPError, Timeout
import threading


class NetworkCrawlerClient(object):

    def __init__(self, network: str = "testnet"):
        if network.lower() not in ["main", "mainnet", "test", "testnet"]:
            raise ValueError("Parameter network - {} - is not valid, requires main, mainnent, test, or testnet.".format(network))

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
        self.sentry_status_request()
        self.active_sentry_api_ip = self.active_sentry_api_list[random.randint(a=0, b=len(self.active_sentry_api_list)-1)]

    def validator_crawler_mp(self):
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

    def validator_status_request(self, validator_ip):
        validator_status = {}
        try:
            process_peer = True
            validator_status["ip"] = validator_ip
            i = Request(api_url="http://{}:26657".format(validator_ip), timeout=1).get(path='/net_info')
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
                s = Request(api_url="http://{}:26657".format(validator_ip), timeout=1).get(path='/status')
            except (ValueError, ConnectionError, HTTPError, Timeout) as e:
                validator_status["validator_status"] = "Unknown - Cannot Connect to Retrieve Status end point - {}".format(e)
                validator_status["connected_nodes"] = []
                process_peer = False

            if process_peer:
                validator_status = self.parse_validator_status(request_json=s, validator_ip=validator_ip)
                validator_status["validator_status"] = "Active"
                validator_status["connected_nodes"] = connected_nodes

        return validator_status

    def parse_validator_status(self, request_json, validator_ip):
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

    def sentry_status_request(self):
        for active_validator in self.active_validator_list:
            try:
                Request(api_url="http://{}:5001".format(active_validator), timeout=1).get(path='/get_status')
                self.active_sentry_api_list.append(active_validator)
            except (ValueError, ConnectionError, HTTPError, Timeout):
                pass
        self.active_sentry_api_list = list(dict.fromkeys(self.active_sentry_api_list))

    def update_validators_and_sentries(self):
        threading.Timer(5.0, self.update_validators_and_sentries).start()
        self.validator_crawler_mp()
        self.sentry_status_request()
        self.active_sentry_api_ip = self.active_sentry_api_list[random.randint(a=0, b=len(self.active_sentry_api_list)-1)]

    def tradehub_get_request(self, path: str, params=None):
        try:
            req = Request(api_url="http://{}:5001".format(self.active_sentry_api_ip), timeout=2).get(path=path, params=params)
            return req
        except (ValueError, ConnectionError, HTTPError, Timeout):
            self.active_sentry_api_list.remove(self.active_sentry_api_ip)
            if not self.active_sentry_api_list:
                self.validator_crawler_mp()
                self.sentry_status_request()
            self.active_sentry_api_ip = self.active_sentry_api_list[random.randint(a=0, b=len(self.active_sentry_api_list)-1)]
            return self.tradehub_get_request(path=path, params=params)

    def tradehub_post_request(self, path: str, data=None, json_data=None, params=None):
        try:
            req = Request(api_url="http://{}:5001".format(self.active_sentry_api_ip), timeout=2).post(self, path=path, data=data, json_data=json_data, params=params)
            return req
        except (ValueError, ConnectionError, HTTPError, Timeout):
            self.active_sentry_api_list.remove(self.active_sentry_api_ip)
            if not self.active_sentry_api_list:
                self.validator_crawler_mp()
                self.sentry_status_request()
            self.active_sentry_api_ip = self.active_sentry_api_list[random.randint(a=0, b=len(self.active_sentry_api_list)-1)]
            return self.tradehub_post_request(path=path, data=data, json_data=json_data, params=params)
