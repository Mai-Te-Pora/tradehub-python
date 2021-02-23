from tradehub.decentralized_client import NetworkCrawlerClient
from tests import APITestCase


class TestNetworkCrawlerClient(APITestCase):

    def setUp(self) -> None:
        self.tradehub_client = NetworkCrawlerClient(network='mainnet')

    def test_validator_crawler_mp(self):
        self.tradehub_client.validator_crawler_mp()
        self.assertIsNotNone(self.tradehub_client.active_sentry_api_list)
        self.assertIsNotNone(self.tradehub_client.active_validator_list)

    def test_validator_status_request(self):
        expect: dict = {
            'moniker': str,
            'id': str,
            'ip': str,
            'version': str,
            'network': str,
            'latest_block_hash': str,
            'latest_block_height': str,
            'latest_block_time': str,
            'earliest_block_height': str,
            'earliest_block_time': str,
            'catching_up': bool,
            'validator_address': str,
            'validator_pub_key_type': str,
            'validator_pub_key': str,
            'validator_voting_power': str,
            'validator_status': str,
            'connected_nodes': [{
                'node_id': str,
                'node_ip': str,
                'node_full': str,
            }]
        }

        result = self.tradehub_client.validator_status_request(validator_ip=self.tradehub_client.active_sentry_api_ip)
        print(result)
        self.assertDictStructure(expect, result)

    def test_parse_validator_status(self):
        expect: dict = {
            'moniker': str,
            'id': str,
            'ip': str,
            'version': str,
            'network': str,
            'latest_block_hash': str,
            'latest_block_height': str,
            'latest_block_time': str,
            'earliest_block_height': str,
            'earliest_block_time': str,
            'catching_up': bool,
            'validator_address': str,
            'validator_pub_key_type': str,
            'validator_pub_key': str,
            'validator_voting_power': str,
        }

        validator_status_json: dict = {
            'jsonrpc': '2.0',
            'id': -1,
            'result': {
                'node_info': {
                    'protocol_version': {
                        'p2p': '7',
                        'block': '10',
                        'app': '0'
                    },
                    'id': '756dece3e0a00705c61a7de701f78f51f5e9a91b',
                    'listen_addr': 'tcp://0.0.0.0:26656',
                    'network': 'switcheo-tradehub-1',
                    'version': '0.33.7',
                    'channels': '4020212223303800',
                    'moniker': 'pike',
                    'other': {
                        'tx_index': 'on',
                        'rpc_address': 'tcp://0.0.0.0:26659'
                    }
                },
                'sync_info': {
                    'latest_block_hash': '3E385BDDF88024B1767BC5E19D4C4F92122FDF16BF93702CCACBD5D1E2299252',
                    'latest_app_hash': '0470CC9EA15482ECB5D497A6D70EF9C1181B649244AB589D8858941FB65EC7FB',
                    'latest_block_height': '7559634',
                    'latest_block_time': '2021-02-16T07:25:24.602077456Z',
                    'earliest_block_hash': 'B4AF1F3D3D3FD5795BDDB7A6A2E6CA4E34D06338505D6EC46DD8F99E72ADCDAB',
                    'earliest_app_hash': '',
                    'earliest_block_height': '1',
                    'earliest_block_time': '2020-08-14T07:32:27.856700491Z',
                    'catching_up': False
                },
                'validator_info': {
                    'address': 'A84B0CB22673DCBCEC8C9EB0A2E83AAC8DE297A2',
                    'pub_key': {
                        'type': 'tendermint/PubKeyEd25519',
                        'value': 'qjqeC/G3OABg7RVbtGDOAS0nWAy3AheJaI7s7OPb5o0='
                    },
                    'voting_power': '0'
                }
            }
        }

        result = self.tradehub_client.parse_validator_status(request_json=validator_status_json, validator_ip=self.tradehub_client.active_sentry_api_ip)
        self.assertDictStructure(expect, result)

    def test_sentry_status_request(self):
        self.tradehub_client.sentry_status_request()
        self.assertIsNotNone(self.tradehub_client.active_sentry_api_list)

    def test_tradehub_get_request(self):
        expect: dict = {
            "jsonrpc": str,
            "id": int,
            "result": {
                "node_info": {
                    "protocol_version": {
                        "p2p": str,
                        "block":  str,
                        "app":  str,
                    },
                    "id": str,
                    "listen_addr": str,
                    "network": str,
                    "version": str,
                    "channels": str,
                    "moniker": str,
                    "other": {
                        "tx_index": str,
                        "rpc_address": str,
                    }
                },
                "sync_info": {
                    "latest_block_hash": str,
                    "latest_app_hash": str,
                    "latest_block_height": str,
                    "latest_block_time": str,
                    "earliest_block_hash": str,
                    "earliest_app_hash": str,
                    "earliest_block_height": str,
                    "earliest_block_time": str,
                    "catching_up": bool
                },
                "validator_info": {
                    "address": str,
                    "pub_key": {
                        "type": str,
                        "value": str,
                    },
                    "voting_power": str,
                }
            }
        }

        result = self.tradehub_client.tradehub_get_request(path='/get_status')
        self.assertDictStructure(expect, result)

        # This Sentry IP should fail and retry with an existing Sentry IP in the active list.
        self.tradehub_client.active_sentry_api_ip = "116.202.216.145"
        self.tradehub_client.active_sentry_api_list.append("116.202.216.145")
        result = self.tradehub_client.tradehub_get_request(path='/get_status')
        self.assertDictStructure(expect, result)
