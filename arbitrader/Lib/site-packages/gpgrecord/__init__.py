import os
import json
import base64
import gnupg
import uuid
import hashlib


gpg = gnupg.GPG()
gpg.encoding = 'utf-8'

def list_recipients():
    return [{"uids": item.get('uids'),
      "fingerprint": item.get('fingerprint')}
     for item in gpg.list_keys()]

def gpg_encrypt_dict(data, recipients, b64=True):
    """
    :recipients = list of fingerprints, or e-mails
    """
    encrypted_data  = gpg.encrypt(
        json.dumps(data), recipients, always_trust=True)

    if not encrypted_data.status == 'encryption ok':
        raise Exception("Encryption failed. {}".format(
            encrypted_data.stderr))

    if b64:
        return str(
            base64.b64encode(
                bytes(
                    str(
                        encrypted_data), 'ascii')), 'ascii')
    else:
        return str(encrypted_data)


def gpg_decrypt_dict(data, b64=True):
    """
    :data: the gpg message, may be b64 encoded
    """

    if b64:
        data = str(base64.b64decode(data), 'ascii')

    decrypted_data = json.loads(str(gpg.decrypt(data)))
    return decrypted_data


def decrypt_data(encrypted_ooio_data):
    """
    :encrypted_ooio_data: data, that has GPG identidies
    """
    payload = encrypted_ooio_data.get('_:b64payload')
    if payload:
        try:
            return gpg_decrypt_dict(payload)
        except:
            raise Exception("Something wrong with payload={}".format(payload))
    else:
        raise Exception("Key not found: '_:b64payload'. Check if GPG key {} is available, and make sure to export GPG_TTY=`tty` or alternative.".format(
            encrypted_ooio_data.get('_:identities')))


def encrypt_data(data, fingerprints):
    """
    >>> fingerprints = ['5AFDB16B89805133F450688BDA580D1D5F5CC7AD']
    >>> data = {
        'password': 'something',
        'username': 'x.makery@gmail.com'
    }
    """

    if isinstance(fingerprints, str):
        fingerprints = [fingerprints]


    return {
        '_:identities': fingerprints,
        '_:b64payload': gpg_encrypt_dict(data, fingerprints)
    }
