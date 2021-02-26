"""
Description:

    Wallet Class for signing, generating, and interacting with a Tradehub account.
    This client is called as part of the Authenticated Client and the Demex Client.
    This class is designed to generate mnemonics, convert mnemonics, private keys, public keys, and addresses.

Usage::

    from tradehub.wallet import Wallet
"""

import base64
import bech32
import ecdsa
import hashlib
import hdwallets
import mnemonic

from tradehub.utils import sort_and_stringify_json


class Wallet(object):
    """
    This class allows the user to interact with the Demex and Tradehub wallet functions.
    Execution of this function is as follows::

        Wallet(mnemonic='lorem ipsum dolor consectetur adipiscing eiusmod tempor incididunt labore magna',
               network='mainnet')
    """

    _DEFAULT_DERIVATION_PATH = "m/44'/118'/0'/0/0"

    def __init__(self, mnemonic: str = None, network: str = "testnet"):
        """
        :param mnemonic: The 12 or 24 word seed required to access your wallet and trade on Demex
        :type mnemonic: str
        :param network: The network you want to interact with. Accepts "testnet" or "mainnet".
        :type network: str
        """
        self.DEFAULT_BECH32_PREFIX_DICT = {
            "main": "swth",
            "mainnet": "swth",
            "test": "tswth",
            "testnet": "tswth",
        }
        self.DEFAULT_BECH32_PREFIX = self.DEFAULT_BECH32_PREFIX_DICT[network.lower()]

        if mnemonic and len(mnemonic.split()) in [12, 24]:
            self._mnemonic = mnemonic
        else:
            self._mnemonic = self.generate_12_word_wallet()

        self._private_key = self.mnemonic_to_private_key(mnemonic_phrase=self._mnemonic)
        self.public_key = self.private_key_to_public_key(private_key=self._private_key)
        self.base64_public_key = base64.b64encode(self.public_key).decode("utf-8")
        self.address = self.private_key_to_address(private_key=self._private_key)

    def generate_12_word_wallet(self):
        """
        Function to generate a 12 word mnemonic.

        Execution of this function is as follows::

            generate_12_word_wallet()

        The expected return result for this function is as follows::

            venture consider cool fury front middle junk person suit assist garbage category

        :return: 12 word String that should be highly protected if storing any funds.
        """
        return mnemonic.Mnemonic(language="english").generate(strength=128)

    def generate_24_word_wallet(self):
        """
        Function to generate a 24 word mnemonic.

        Execution of this function is as follows::

            generate_24_word_wallet()

        The expected return result for this function is as follows::

            refuse flag merge fiction choose dream frown gauge need fabric once pizza actual armed reopen couple family fury reopen slush blue try focus minute

        :return: 24 word String that should be highly protected if storing any funds.
        """
        return mnemonic.Mnemonic(language="english").generate(strength=256)

    def mnemonic_to_private_key(self, mnemonic_phrase: str = None, wallet_path: str = _DEFAULT_DERIVATION_PATH) -> bytes:
        """
        Function to find the private key based on the mnemonic passed to the function.

        Execution of this function is as follows::

            mnemonic_to_private_key(mnemonic_phrase='venture consider cool fury front middle junk person suit assist garbage category',
                                    wallet_path=_DEFAULT_DERIVATION_PATH)

        The expected return result for this function is as follows::

            b'\x15\xcf\xdd\xdf\xead\x88\xd2y!\xdb\xb61\xa6\x98\xeeQm\x05\xed\x8d%43!\n\xccS\xcbsf\x90'

        :param mnemonic_phrase: String mnemonic phrase for a tradehub wallet.
        :param wallet_path: String Derivation path to generated the private key from the mnemonic.
        :return: Byte value that is equal to the private key.
        """
        mnemonic_bytes = mnemonic.Mnemonic.to_seed(mnemonic_phrase, passphrase="")
        hd_wallet = hdwallets.BIP32.from_seed(mnemonic_bytes)
        self._private_key = hd_wallet.get_privkey_from_path(wallet_path)
        return self._private_key

    def private_key_to_public_key(self, private_key: bytes = None) -> bytes:
        """
        Function to find the public key based on the private key passed to the function.

        Execution of this function is as follows::

            private_key_to_public_key(private_key=b'\x15\xcf\xdd\xdf\xead\x88\xd2y!\xdb\xb61\xa6\x98\xeeQm\x05\xed\x8d%43!\n\xccS\xcbsf\x90')

        The expected return result for this function is as follows::

            b'\x02o\x1f\xfbL\x96\xe8\x1e\xb0\x12V\x80\xc7t\xfc\xb40R\xaeu\xf3{\xf6\xd7m]\xd1\xa9\x91\xa8\xe0Df'

        :param private_key: Byte representation of the wallets private key.
        :return: Binary value that is equal to the public key.
        """
        privkey_obj = ecdsa.SigningKey.from_string(self._private_key, curve=ecdsa.SECP256k1)
        self.public_key_obj = privkey_obj.get_verifying_key()
        self.public_key = self.public_key_obj.to_string("compressed")
        return self.public_key

    def public_key_to_address(self, public_key: bytes = None, hrp: str = None) -> str:
        """
        Function to find the readable address from the public key.

        Execution of this function is as follows::

            public_key_to_address(public_key=b'\x02o\x1f\xfbL\x96\xe8\x1e\xb0\x12V\x80\xc7t\xfc\xb40R\xaeu\xf3{\xf6\xd7m]\xd1\xa9\x91\xa8\xe0Df',
                                  hrp=None)

        The expected return result for this function is as follows::

            tswth1upcgussnx4p3jegwj3x2fccwlajwckkzgstrp8

        :param public_key: Byte representation of the wallets public key.
        :return: String and human readable Tradehub address.
        """
        if hrp is None:
            hrp = self.DEFAULT_BECH32_PREFIX
        s = hashlib.new("sha256", public_key).digest()
        r = hashlib.new("ripemd160", s).digest()
        five_bit_r = bech32.convertbits(r, 8, 5)
        assert five_bit_r is not None, "Unsuccessful bech32.convertbits call"
        return bech32.bech32_encode(hrp, five_bit_r)

    def private_key_to_address(self, private_key: bytes = None, hrp: str = None) -> str:
        """
        Function to find the readable address from the private key.

        Execution of this function is as follows::

            public_key_to_address(public_key=b'\x15\xcf\xdd\xdf\xead\x88\xd2y!\xdb\xb61\xa6\x98\xeeQm\x05\xed\x8d%43!\n\xccS\xcbsf\x90',
                                  hrp=None)

        The expected return result for this function is as follows::

            tswth1upcgussnx4p3jegwj3x2fccwlajwckkzgstrp8

        :param private_key: Byte representation of the wallets private key.
        :return: String and human readable Tradehub address.
        """
        if hrp is None:
            hrp = self.DEFAULT_BECH32_PREFIX
        public_key = self.private_key_to_public_key(private_key)
        return self.public_key_to_address(public_key=public_key, hrp=hrp)

    def _sign(self, message: dict) -> str:
        """
        Function to find the readable address from the public key.

        Execution of this function is as follows::

            _sign(message={'message': 'This is a Tradehub test.'})

        The expected return result for this function is as follows::

            XP4s5fCY6UKh/dvscYsDylhYeD64WOTYohEU3QuuUygPCiQF9uFS9mHgwLaTFfFL41mdTRZclxq6CETr8bcZ5w==

        :param message: Dictionary message to sign.
        :return: Signed message.
        """
        message_str = sort_and_stringify_json(message=message)
        message_bytes = message_str.encode("utf-8")

        private_key = ecdsa.SigningKey.from_string(self._private_key, curve=ecdsa.SECP256k1)
        signature_compact = private_key.sign_deterministic(
            message_bytes,
            hashfunc=hashlib.sha256,
            sigencode=ecdsa.util.sigencode_string_canonize
        )

        signature_base64_str = base64.b64encode(signature_compact).decode("utf-8")
        return signature_base64_str
