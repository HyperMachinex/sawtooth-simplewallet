import traceback
import sys
import hashlib
import logging

from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.exceptions import InternalError
from sawtooth_sdk.processor.core import TransactionProcessor

LOGGER = logging.getLogger(__name__)
FAMILY_NAME = "simplewallet"
def _hash(data):
    return hashlib.sha512(data).hexdigest()

# prefix for first six hex digits
sw_namespace = _hash(FAMILY_NAME.encode('utf-8'))[0:6]

#transaction processor class

class SimpleWalletTransactionHandler(TransactionHandler):

    def __init__(self, namespace_prefix):
        self._namespace_prefix = namespace_prefix

    @property
    def family_name(self):
        return FAMILY_NAME

    @property
    def family_versions(self):
        return ['1.0']

    @property
    def namespaces(self):
        return [self._namespace_prefix]
    
    
    def apply(self, transaction, context):
        
        # get payload and parse data
        header = transaction.header
        print(transaction.payload)
        payload_list = transaction.payload.decode().split(",")
        operation = payload_list[0]
        print()
        print(operation)
        amount = int(payload_list[1].lstrip("[").rstrip("]"))
        print()
        print(amount)

        # public key
        from_key = header.signer_public_key

        LOGGER.info("Operation = "+ operation)

        if operation == "deposit":
            self._make_deposit(context, amount, from_key)
        elif operation == "create":
            self._make_create(context, amount, from_key)
        elif operation == "withdraw":
            self._make_withdraw(context, amount, from_key)
        elif operation == "transfer":
            if len(payload_list) == 3:
                print("Transaction prcoessora geldim")
                print()
                print("Payload list")
                print(payload_list)
                print()
                print("Context")
                print(context)
                print()
                to_key = payload_list[2]
            self._make_transfer(context, amount, to_key, from_key)
        else:
            LOGGER.info("Unhandled action. " + "Operation should be deposit, withdraw or transfer")
    
    def _make_create(self, context, amount, from_key):

        # take address
        wallet_address = self._get_wallet_address(from_key)

        LOGGER.info('Got the key {} and the wallet address {} '.format(
            from_key, wallet_address))
        
        # take wallet infos
        current_entry = context.get_state([wallet_address])
        new_balance = 0

        if current_entry == []:
            LOGGER.info('Creating new wallet {} '
                .format(from_key))
            new_balance = int(amount)
        else:
            LOGGER.info('This wallet exists {} '
                .format(from_key))

        state_data = str(new_balance).encode('utf-8')
        addresses = context.set_state({wallet_address: state_data})

        if len(addresses) < 1:
            raise InternalError("State Error")

    def _make_deposit(self, context, amount, from_key):

        # take address
        wallet_address = self._get_wallet_address(from_key)


        LOGGER.info('Got the key {} and the wallet address {} '.format(
            from_key, wallet_address))
        
        # take wallet infos
        current_entry = context.get_state([wallet_address])
        new_balance = 0

        if current_entry == []:
            LOGGER.info('No previous deposits, creating new deposit {} '
                .format(from_key))
            new_balance = int(amount)
        else:
            balance = int(current_entry[0].data)
            new_balance = int(amount) + int(balance)

        state_data = str(new_balance).encode('utf-8')
        addresses = context.set_state({wallet_address: state_data})

        if len(addresses) < 1:
            raise InternalError("State Error")
        
    def _make_withdraw(self, context, amount, from_key):

        wallet_address = self._get_wallet_address(from_key)
        
        LOGGER.info('Got the key {} and the wallet address {} '.format(
            from_key, wallet_address))
        
        
        current_entry = context.get_state([wallet_address])
        new_balance = 0

        if current_entry == []:
            LOGGER.info('No user with the key {} '.format(from_key))
        else:
            balance = int(current_entry[0].data)
            print("balance: ",balance)
            if balance < int(amount):
                raise InvalidTransaction('Not enough money. The amount ' +
                    'should be lesser or equal to {} '.format(balance))
            else:
                new_balance = balance - int(amount)

        LOGGER.info('Withdrawing {} '.format(amount))
        state_data = str(new_balance).encode('utf-8')
        addresses = context.set_state(
            {self._get_wallet_address(from_key): state_data})

        if len(addresses) < 1:
            raise InternalError("State Error")
        
    def _make_transfer(self, context, transfer_amount, to_key, from_key):
        print("Transfere geldim")
        print(f"Context: {context}")
        print(f"From key: {from_key}")
        print(f"To_key: {to_key}")
        transfer_amount = int(transfer_amount)
        if transfer_amount <= 0:
            raise InvalidTransaction("The amount cannot be <= 0")

        wallet_address = self._get_wallet_address(from_key)
        wallet_to_address = self._get_wallet_address(to_key)

        print(f"From wallet address: {wallet_address}")
        print(f"To wallet address: {wallet_to_address}")

        LOGGER.info('Got the from key {} and the from wallet address {} '.format(
            from_key, wallet_address))
        LOGGER.info('Got the to key {} and the to wallet address {} '.format(
            to_key, wallet_to_address))
        current_entry = context.get_state([wallet_address])
        current_entry_to = context.get_state([wallet_to_address])
        new_balance = 0

        if current_entry == []:
            LOGGER.info('No user (debtor) with the key {} '.format(from_key))
        if current_entry_to == []:
            LOGGER.info('No user (creditor) with the key {} '.format(to_key))

        balance = int(current_entry[0].data)
        print()
        print(balance)
        print()
        print (current_entry_to)
        balance_to = int(current_entry_to[0].data)
        if balance < transfer_amount:
            raise InvalidTransaction('Not enough money. ' +
                'The amount should be less or equal to {} '.format(balance))
        else:
            LOGGER.info("Debiting balance with {}".format(transfer_amount))
            update_debtor_balance = balance - int(transfer_amount)
            state_data = str(update_debtor_balance).encode('utf-8')
            context.set_state({wallet_address: state_data})
            update_beneficiary_balance = balance_to + int(transfer_amount)
            state_data = str(update_beneficiary_balance).encode('utf-8')
            context.set_state({wallet_to_address: state_data})
    
    def _get_wallet_address(self, key):
        return _hash(FAMILY_NAME.encode('utf-8'))[0:6] + _hash(key.encode('utf-8'))[0:64]


def setup_loggers():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    
def main():
    
    
    #entry point
    setup_loggers()
    try:
        # Register the transaction handler and start it.
        processor = TransactionProcessor(url='tcp://validator:4004')

        handler = SimpleWalletTransactionHandler(sw_namespace)

        processor.add_handler(handler)

        processor.start()

    except KeyboardInterrupt:
        pass
    except SystemExit as err:
        raise err
    except BaseException as err:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

