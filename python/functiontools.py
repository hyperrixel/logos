"""
Logos - a mission toolkit for cooperative logging through space and time
------------------------------------------------------------------------

Submodule: functiontools
"""


from base64 imort 
from enum import Enum
from hashlib import sha256
import json
from time import time

import rsa


def bytes_to_dict(data : bytes) -> dict:
    """
    Convert bytes to dict
    =====================

    Parameters
    ----------
    data : bytes
        Data to convert.

    Returns
    -------
    dict
        The converted data.
    """

    return json.loads(data.decode('utf-8'))


def check_data(data : dict, keys : list) -> bool:
    """
    Check if data is a dict and contains required key(s)
    ====================================================

    Parameters
    ----------
    data : dict
        Data to check.
    keys : list
        Keys to check.

    Returns
    -------
    bool
        True on success.

    Raises
    ------
    LogosSerializationError
        When the given data is not a dict.
    LogosSerializationError
        When the given data doesn't contain the needed keys.
    """

    if not isinstance(data, dict):
        raise LogosSerializationError('Data must be converted to dict.')
    if not all([key in data.keys() for key in keys]):
        raise LogosSerializationError('Data must contain key(s) "{}".'
                                      .format(', '.join(keys)))
    return True


def check_switch(panel : int, switch : int) -> bool:
    """
    Get whether switch is set on or off
    ===================================

    Parameters
    ----------
    panel : int
        Switch panel to investigate.
    switch : int
        Switch to check.

    Returns
    -------
    bool
        True, if switch is on, False if not.

    Notes
    -----
        This function works well binary switch panels only.
    """

    return panel // switch % 2 == 1


def decrypt_rsa(data : bytes, private_key : rsa.key.PrivateKey) -> bytes:
    """
    Decrypt data with the given key
    ===============================

    Parameters
    ----------
    data : str
        Data to encrypt.
    public_key : rsa.key.PrivateKey
        Public key to encrypt with.

    Returns
    -------
    bytes
        Encrypted data
    """

    return rsa.decrypt(data, private_key)


def dict_to_bytes(data : dict) -> bytes:
    """
    Convert dict to bytes
    =====================

    Parameters
    ----------
    data : dict
        Data to convert.

    Returns
    -------
    bytes
        The converted data.
    """

    return json.dumps(data).encode('utf-8')


def encrypt_rsa(data : bytes, public_key : rsa.key.PublicKey) -> bytes:
    """
    Encrypt data with the given key
    ===============================

    Parameters
    ----------
    data : str
        Data to encrypt.
    public_key : rsa.key.PublicKey
        Public key to encrypt with.

    Returns
    -------
    bytes
        Encrypted data
    """

    return rsa.encrypt(data, public_key)


def generate_rsa_keys(strength : int = 2048) -> dict:
    """
    Generate rsa keys
    =================

    Parameters
    ----------
    strength : int, optional (2048 if omitted)
        Length of the key to generate.

    Returns
    -------
    dict(public_key : rsa.key.PublicKey, private_key : rsa.key.PrivateKey)
        Generated RSA public and private keys.
    """

    public_key, private_key = rsa.newkeys(strength)
    return {'public_key' : public_key, 'private_key' : private_key}


def get_data_hash(data : bytes) -> bytes:
    """
    Get hash from data
    ==================

    Parameters
    ----------
    data : bytes
        Binary content to get hasehed.

    Returns
    -------
    bytes
        The hash of the content.
    """

    return sha256(content).digest()


def get_hash(content : str) -> bytes:
    """
    Get hash from string
    ====================

    Parameters
    ----------
    content : str
        Text content to get hasehed.

    Returns
    -------
    bytes
        The hash of the content.
    """

    return sha256(content.encode('utf-8')).digest()


def get_package_template(is_response : bool = False,
                         is_micro : bool = False) -> dict:
    """
    Get package template
    ====================

    Parameters
    ----------
    is_response : bool, optional (False if omitted)
        Whether the package is a data package (default) or response pacakage.
    is_micro : bool, optional (False if omitted)
        Whether the package is micro package or not.

    Rerurns
    -------
    dict
        Dict with package keys and basic informations.
    """

    if not is_micro:
        if not is_response:
            result = {'PackageType' : 'Logos',
                      'PackageVersion' : [0, 0, 1, 'dev'],
                      'PackageID' : '',
                      'Operation' : '',
                      'Content' : bytes()}
        else:
            result = {'PackageType' : 'Logos_response',
                      'PackageVersion' : [0, 0, 1, 'dev'],
                      'PackageID' : '',
                      'PackageHash' : bytes(),
                      'QueryInterval' : [0, 100]}
    else:
        if not is_response:
            result = ['', '', bytes()]
        else:
            result = ['', bytes(), [0, 100]]
    return result


def now() -> int:
    """
    Get millisecond precision int timestamp
    =======================================
    """

    return round(time() * 1000)


def rsa_key_to_str(key_data : any) -> str:
    """
    Transform key to string
    =======================

    Parameters
    ----------
    key_data : rsa.key.PublicKey | rsa.key.PrivateKey
        Key to transform.

    Returns
    -------
    str
        Transformed key to PKCS1 PEM format.
    """

    return key_data.save_pkcs1().decode('utf-8')


def rsa_keys_to_dict(key_data : dict) -> dict:
    """
    Transform keys to string
    ========================

    Parameters
    ----------
    key_data : dict
        Keys to transform. Data must have the form of:
        dict(public_key : rsa.key.PublicKey, private_key : rsa.key.PrivateKey)

    Returns
    -------
    dict(public_key : str, private_key : str)
        Transformed keys to PKCS1 PEM format.
    """

    return {'public_key' : rsa_key_to_str(key_data['public_key']),
            'private_key' : rsa_key_to_str(key_data['private_key']),}


def rsa_dict_to_keys(key_dict : dict) -> dict:
    """
    Transform dict to RSA key pair
    ==============================

    Parameters
    ----------
    key_dict : dict('public_key' : str, 'private_key' : str)
        Dict to transform.

    Returns:
    dict(public_key : rsa.key.PublicKey, private_key : rsa.key.PrivateKey)
        Key pair dict.
    """

    return {'public_key' : rsa_str_to_public_key(key_dict['public_key']),
            'private_key' : rsa_str_to_private_key(key_dict['private_key'])}


def rsa_str_to_private_key(key_str : str) -> rsa.key.PrivateKey:
    """
    Transform string to RSA private key
    ===================================

    Parameters
    ----------
    key_str : str
        String to transform.

    Returns:
    rsa.key.PrivateKey
        Private key object.
    """

    return rsa.key.PrivateKey.load_pkcs1(key_str.encode('utf-8'))


def rsa_str_to_public_key(key_str : str) -> rsa.key.PublicKey:
    """
    Transform string to RSA public key
    ==================================

    Parameters
    ----------
    key_str : str
        String to transform.

    Returns:
    rsa.key.PrivateKey
        Public key object.
    """

    return rsa.key.PublicKey.load_pkcs1(key_str.encode('utf-8'))
