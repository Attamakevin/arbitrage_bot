from . import encrypt_data, decrypt_data

def test_crypt():
    data = {'hello': 'world'}
    result = decrypt_data(encrypt_data(
            {'hello': 'world'},
            '5AFDB16B89805133F450688BDA580D1D5F5CC7AD')
    )

    assert data == result
