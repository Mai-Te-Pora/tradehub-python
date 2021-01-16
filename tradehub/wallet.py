import base64
import bech32
import ecdsa
import hashlib
import hdwallets
import mnemonic

from hdwallets import BIP32DerivationError as BIP32DerivationError
from tradehub.utils import sort_and_stringify_json


class Wallet(object):

    _DEFAULT_DERIVATION_PATH = "m/44'/118'/0'/0/0"

    def __init__(self, mnemonic: str, network: str = "testnet"):
        """

        """
        self.DEFAULT_BECH32_PREFIX_DICT = {
            "mainnet": "swth",
            "testnet": "tswth",
        }
        self.DEFAULT_BECH32_PREFIX = self.DEFAULT_BECH32_PREFIX_DICT[network]

        if mnemonic:
            self._mnemonic = mnemonic
            self._private_key = self.mnemonic_to_private_key(mnemonic_phrase = self._mnemonic)
            self.public_key = self.private_key_to_public_key(private_key = self._private_key)
            self.base64_public_key = base64.b64encode(self.public_key).decode("utf-8")
            self.address = self.private_key_to_address(private_key = self._private_key)
        else:
            self._private_key = None
            self.public_key = None
            self.public_key_obj = None
            self.base64_public_key = None
            self.address = None


    def generate_wallet(self):
        return mnemonic.Mnemonic(language = "english").generate(strength = 256)

    def mnemonic_to_private_key(self, mnemonic_phrase: str = None, wallet_path: str = _DEFAULT_DERIVATION_PATH) -> bytes:
        mnemonic_bytes = mnemonic.Mnemonic.to_seed(mnemonic_phrase, passphrase = "")
        hd_wallet = hdwallets.BIP32.from_seed(mnemonic_bytes)
        self._private_key = hd_wallet.get_privkey_from_path(wallet_path)
        return self._private_key

    def private_key_to_public_key(self, private_key: bytes = None) -> bytes:
        privkey_obj = ecdsa.SigningKey.from_string(self._private_key, curve = ecdsa.SECP256k1)
        self.public_key_obj = privkey_obj.get_verifying_key()
        self.public_key = self.public_key_obj.to_string("compressed")
        return self.public_key

    def public_key_to_address(self, public_key: bytes = None, hrp: str = None) -> str:
        if hrp is None:
            hrp = self.DEFAULT_BECH32_PREFIX
        s = hashlib.new("sha256", public_key).digest()
        r = hashlib.new("ripemd160", s).digest()
        five_bit_r = bech32.convertbits(r, 8, 5)
        assert five_bit_r is not None, "Unsuccessful bech32.convertbits call"
        return bech32.bech32_encode(hrp, five_bit_r)

    def private_key_to_address(self, private_key: bytes = None, hrp: str = None) -> str:
        if hrp is None:
            hrp = self.DEFAULT_BECH32_PREFIX
        public_key = self.private_key_to_public_key(private_key)
        return self.public_key_to_address(public_key = public_key, hrp = hrp)

    def _sign(self, message: dict) -> str:
        message_str = sort_and_stringify_json(message = message)
        message_bytes = message_str.encode("utf-8")

        private_key = ecdsa.SigningKey.from_string(self._private_key, curve = ecdsa.SECP256k1)
        signature_compact = private_key.sign_deterministic(
            message_bytes,
            hashfunc = hashlib.sha256,
            sigencode = ecdsa.util.sigencode_string_canonize
        )

        signature_base64_str = base64.b64encode(signature_compact).decode("utf-8")
        return signature_base64_str
