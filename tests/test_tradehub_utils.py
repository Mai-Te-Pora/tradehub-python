import tradehub.utils as utils
from tests import APITestCase, NEO_ADDRESS, NEO_CONTRACT, ETH_ADDRESS, ETH_CONTRACT, WEB3_API_URL


class TestTradeHubUtils(APITestCase):

    def setUp(self) -> None:
        self.r = utils.Request(api_url='https://jsonplaceholder.typicode.com/')
        self.s = utils.Request()

    def test_request_get(self):
        json_msg = {
            "userId": 1,
            "id": 1,
            "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
            "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"}
        self.assertDictEqual(self.r.get(path='/posts/1'), json_msg)

    def test_request_post(self):
        json_dict = {
            'title': 'foo',
            'body': 'bar',
            'userId': 1}
        json_msg = {
            'id': 101,
            'title': 'foo',
            'body': 'bar',
            'userId': 1}
        self.assertDictEqual(self.r.post(path='/posts', json_data=json_dict), json_msg)

    def test_request_status(self):
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

        self.assertDictStructure(expect, self.s.status())

    def test_sort_and_stringify_json(self):
        json_msg = {"name": "John Smith", "age": 27, "siblings": ["Jane", "Joe"]}
        stringify_msg = '{"age":27,"name":"John Smith","siblings":["Jane","Joe"]}'
        self.assertEqual(utils.sort_and_stringify_json(json_msg), stringify_msg)

    def test_to_tradehub_asset_amount(self):
        self.assertEqual(utils.to_tradehub_asset_amount(amount=float('123.4567')), '12345670000')
        self.assertEqual(utils.to_tradehub_asset_amount(amount=float('123.4567'), decimals=16), '1234567000000000000')

    def test_reverse_hex(self):
        self.assertEqual(utils.reverse_hex('ABCD'), 'CDAB')
        self.assertEqual(utils.reverse_hex('0000000005f5e100'), '00e1f50500000000')

    def test_is_valid_neo_public_address(self):
        self.assertTrue(utils.is_valid_neo_public_address(address=NEO_ADDRESS))
        self.assertFalse(utils.is_valid_neo_public_address(address=NEO_CONTRACT))

    def test_neo_get_scripthash_from_address(self):
        self.assertEqual(utils.neo_get_scripthash_from_address(address=NEO_ADDRESS), 'fea2b883725ef2d194c9060f606cd0a0468a2c59')

    def test_is_eth_contract(self):
        self.assertTrue(utils.is_eth_contract(address=ETH_CONTRACT,
                                              web3_uri=WEB3_API_URL))
        self.assertFalse(utils.is_eth_contract(address=ETH_ADDRESS,
                                               web3_uri=WEB3_API_URL))

    def test_format_withdraw_address(self):
        valid_neo_address = utils.format_withdraw_address(address=NEO_ADDRESS, blockchain='neo')
        self.assertEqual(valid_neo_address, '592c8a46a0d06c600f06c994d1f25e7283b8a2fe')
        with self.assertRaises(ValueError):
            utils.format_withdraw_address(address=NEO_CONTRACT, blockchain='neo')
        valid_eth_address = utils.format_withdraw_address(address=ETH_ADDRESS, blockchain='eth', web3_uri=WEB3_API_URL)
        self.assertEqual(valid_eth_address, '32c46323b51c977814E05EF5E258Ee4da0E4c3c3')
        with self.assertRaises(ValueError):
            utils.format_withdraw_address(address=ETH_CONTRACT, blockchain='eth', web3_uri=WEB3_API_URL)
