#!/usr/bin/env python3
import argparse
import logging
from client import *

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

def transfer(wallet_name, dest_wallet, transfer):
    main_keyfile = f'/root/.sawtooth/keys/{wallet_name}.priv'
    dest_keyfile = f'/root/.sawtooth/keys/{dest_wallet}.priv'
    client = SimpleWalletClient(baseUrl='http://rest-api:8008', keyFile=main_keyfile)
    client2 = SimpleWalletClient(baseUrl='http://rest-api:8008', keyFile=dest_keyfile)
    LOGGER.info(f"Transfer money from {wallet_name} to {dest_wallet}")
    print(f'Destination:{dest_keyfile}')
    client.transfer(transfer, dest_wallet)

def main():
    parser = argparse.ArgumentParser(description='Trasfer')
    #parser.add_argument('-r', '--swallet', type=str, required=True, help='Name of the source wallet')
    #parser.add_argument('-d', '--dwallet', type=str, required=True, help='Name of the destination wallet')
    #parser.add_argument('-p', '--value', type = int, nargs='+', required=True, help='Money to transfer')
    parser.add_argument("swallet", type = str, help= 'Name of the source wallet')
    parser.add_argument("dwallet", type = str, help= 'Name of the destination wallet')
    parser.add_argument("value", type = int, help= 'Money to transfer')
    args = parser.parse_args()
    transfer(args.swallet, args.dwallet, args.value)

if __name__ == '__main__':
    main()
