#!/usr/bin/env python3
import argparse
import logging
from client import *
FAMILY_NAME = "simplewallet"
def _hash(data):
    return hashlib.sha512(data).hexdigest()

# prefix for first six hex digits
sw_namespace = _hash(FAMILY_NAME.encode('utf-8'))[0:6]

def _get_wallet_addresss(key):
    return _hash(FAMILY_NAME.encode('utf-8'))[0:6] + _hash(key.encode('utf-8'))[0:64]


# This file is for debug use.

def main():
    from_key = 'b41665e83de3f4b3feb05cd2249cf4b58e2a2abbead618678bb8cb02b1d894b1'
    wallet_address = _get_wallet_addresss(from_key)
    print(f'From Wallet addres priv:{wallet_address}')

    from_key2 = '022faf2213259d436f4af1dce703626663dcec71c17b4c255be4de221628ffb342'
    wallet_address = _get_wallet_addresss(from_key2)
    print(f'From Wallet addres pub:{wallet_address}')

    
    to_key = '9c6e01f5acc841385837b7436922157da2183c43d392abaa42b0cb3e0836e401'
    wallet_address = _get_wallet_addresss(to_key)
    print(f'To Wallet addres priv:{wallet_address}')

    to_key2 = '02dca6a6a26c1a8346b0f6878e9239f8841f190931c798dfed8d792c7763950391'
    wallet_address = _get_wallet_addresss(to_key2)
    print(f'To Wallet addres pub:{wallet_address}')

if __name__ == '__main__':
    main()
