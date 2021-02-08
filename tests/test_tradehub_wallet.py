from unittest import TestCase
from tests import WALLET_MNEMONIC, WALLET_PRIVATE_KEY, WALLET_PUBLIC_KEY, WALLET_ADDRESS
from tradehub.wallet import Wallet


class TestTradeHubGenerateWallet(TestCase):

    def setUp(self) -> None:
        self._wallet = Wallet(mnemonic=WALLET_MNEMONIC)

    def test_get_12_word_wallet(self):
        """
        Check if Wallet generates a 12 word mnemonic.
        :return:
        """

        result: str = self._wallet.generate_12_word_wallet()
        self.assertIsInstance(result, str, msg="Expected result to be type {}, got {} instead.".format("str", type(result)))
        self.assertEqual(len(result.split()), 12)

    def test_get_24_word_wallet(self):
        """
        Check if Wallet generates a 24 word mnemonic.
        :return:
        """

        result: str = self._wallet.generate_24_word_wallet()
        self.assertIsInstance(result, str, msg="Expected result to be type {}, got {} instead.".format("str", type(result)))
        self.assertEqual(len(result.split()), 24)

    def test_mnemonic_to_private_key(self):
        """
        Check if Wallet Private Key derivation is accurate.
        :return:
        """

        result: bytes = self._wallet.mnemonic_to_private_key(mnemonic_phrase=WALLET_MNEMONIC)
        self.assertIsInstance(result, bytes, msg="Expected result to be type {}, got {} instead.".format("bytes", type(result)))
        self.assertEqual(result, WALLET_PRIVATE_KEY)

    def test_private_key_to_public_key(self):
        """
        Check if Wallet Public Key derived from the Private Key is as expected.
        :return:
        """

        result: bytes = self._wallet.private_key_to_public_key(private_key=WALLET_PRIVATE_KEY)
        self.assertIsInstance(result, bytes, msg="Expected result to be type {}, got {} instead.".format("bytes", type(result)))
        self.assertEqual(result, WALLET_PUBLIC_KEY)

    def test_public_key_to_address(self):
        """
        Check if Wallet Address derived from the Public Key is as expected.
        :return:
        """

        result: str = self._wallet.public_key_to_address(public_key=WALLET_PUBLIC_KEY, hrp="tswth")
        self.assertIsInstance(result, str, msg="Expected result to be type {}, got {} instead.".format("str", type(result)))
        self.assertEqual(result, WALLET_ADDRESS)

    def test_private_key_to_address(self):
        """
        Check if Wallet Address derived from the Private Key is as expected.
        :return:
        """

        result: str = self._wallet.private_key_to_address(private_key=WALLET_PRIVATE_KEY, hrp="tswth")
        self.assertIsInstance(result, str, msg="Expected result to be type {}, got {} instead.".format("str", type(result)))
        self.assertEqual(result, WALLET_ADDRESS)

    def test_signing(self):
        """
        Check if Signature returns the expected results.
        :return:
        """

        result: str = self._wallet._sign(message="Hello Switcheo")
        self.assertIsInstance(result, str, msg="Expected result to be type {}, got {} instead.".format("str", type(result)))
        self.assertEqual(result, '104CCiE3SxWHhB0LI5apCOsC68CrNIcCIragNhr8ok0K8eoL+tuxDnKQ/BpBRT75oGxdh6g9nzAiV9t0KajYFQ==')
