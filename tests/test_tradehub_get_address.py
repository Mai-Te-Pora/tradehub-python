from tests import APITestCase, DEVEL_AND_CO_SENTRY
from tradehub.public_client import PublicClient


class TestTradeHubGetAddress(APITestCase):

    def setUp(self) -> None:
        self._client = PublicClient(DEVEL_AND_CO_SENTRY)

    def test_get_address_structure(self):
        """
        Check if response match expected dict structure.
        :return:
        """
        expect: str = "swth1qlue2pat9cxx2s5xqrv0ashs475n9va963h4hz"

        result: str = self._client.get_address("devel484")

        # Check type
        self.assertIsInstance(result, str)
        # Check value
        self.assertEqual(result, expect)
