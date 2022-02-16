from eventsourcing.domain import Aggregate, event
from uuid import uuid5, NAMESPACE_URL


class Account(Aggregate):
    """A simple-as-can-be bank account"""

    @event('Created')
    def __init__(self):
        self.balance = 0

    @event('Credited')
    def credit(self, amount: int):
        self.balance += amount

    @event('Debited')
    def debit(self, amount: int):
        self.balance -= amount


class Ledger(Aggregate):
    """A simple-as-can-be Ledger to track net movements across all accounts"""
    def __init__(self, name):
        self.name = name
        self.transaction_count = 0
        self.balance = 0

    @classmethod
    def create_id(cls, name):
        """Enable predictable IDs so that a Ledger can be retrieved
           using its name - even if its ID isn't known
        """
        return uuid5(NAMESPACE_URL, f'/ledgers/{name}')

    @event('TransactionAdded')
    def add_transaction(self, amount: int):
        self.transaction_count += 1
        self.balance += amount

    def get_balance(self):
        return self.balance

    def get_transaction_count(self):
        return self.transaction_count
