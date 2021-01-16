from tests import APITestCase, DEVEL_AND_CO_SENTRY
from tradehub.public_client import PublicClient


class TestTradeHubGetStatus(APITestCase):

    def setUp(self) -> None:
        self._client = PublicClient(DEVEL_AND_CO_SENTRY)

    def test_get_status_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """

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

        result: dict = self._client.get_status()

        self.assertDictStructure(expect, result)