"""Create Bitcoin addresses from passphrases or private keys.

This module provides the :class:`Wallet` class which is a small wrapper around
``coinkit.BitcoinKeypair``.  It is used by ``bbb.py`` to convert dictionary
words or encoded private keys into Bitcoin addresses and associated key
pairs.
"""

from coinkit import BitcoinKeypair
import logging


class Wallet:
    """Generate a Bitcoin wallet from a passphrase or private key.

    Parameters
    ----------
    passphrase : str
        Secret used to create the wallet.  This may either be a brain wallet
        passphrase or a hex/WIF encoded private key depending on
        ``is_private_key``.
    is_private_key : bool, optional
        When ``True`` the ``passphrase`` argument is interpreted as a private
        key.  Otherwise it will be treated as a brain wallet passphrase.

    Attributes
    ----------
    passphrase : str
        The original secret supplied during construction.
    address : str
        The generated Bitcoin address.
    public_key : str
        The generated public key.
    private_key : str
        The generated private key.
    """

    def __init__(self, passphrase, is_private_key = False):
        self.passphrase = passphrase
        self.address = None
        self.public_key = None
        self.private_key = None
        try:
            if is_private_key:
                keypair = BitcoinKeypair.from_private_key(self.passphrase.encode('ascii'))
            else:
                keypair = BitcoinKeypair.from_passphrase(self.passphrase)
            self.address = keypair.address()
            self.public_key = keypair.public_key()
            self.private_key = keypair.private_key()
        except Exception as e:
            logging.warning(u"Failed to generate keypair for passphrase '{}'. Error: {}".format(passphrase, e.args))
            raise