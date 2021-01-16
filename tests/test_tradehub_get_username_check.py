from tests import APITestCase, DEVEL_AND_CO_SENTRY, USERNAME_DEVEL
from tradehub.public_client import PublicClient


class TestTradeHubGetUsernameCheck(APITestCase):

    def setUp(self) -> None:
        self._client = PublicClient(DEVEL_AND_CO_SENTRY)

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
