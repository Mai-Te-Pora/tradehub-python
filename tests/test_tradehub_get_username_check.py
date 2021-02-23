from tests import APITestCase, mainnet_client, USERNAME_DEVEL


class TestTradeHubGetUsernameCheck(APITestCase):

    def setUp(self) -> None:
        self._client = mainnet_client

    def test_get_username_check_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """

        result: bool = self._client.get_username_check(USERNAME_DEVEL)

        self.assertIsInstance(result, bool, msg=f"Expected result to be type bool, got {type(result)} instead.")
        # TODO need test wallet
        self.assertTrue(result, msg=f"Expected username {USERNAME_DEVEL} to be taken.")

        result: bool = self._client.get_username_check(USERNAME_DEVEL.upper())
        self.assertIsInstance(result, bool, msg=f"Expected result to be type bool, got {type(result)} instead.")

        self.assertFalse(result, msg=f"Expected username {USERNAME_DEVEL.upper()} to be not taken.")
