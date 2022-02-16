from eventsourcing.application import AggregateNotFound
from eventsourcing.system import ProcessApplication
from eventsourcing.dispatch import singledispatchmethod
from event_sourced_bank.domain_model import Account, Ledger
import logging

ledger_name = "General"


class LedgerService(ProcessApplication):
    @singledispatchmethod
    def policy(self, domain_event, process_event):
        """Default policy"""

    @policy.register(Account.Credited)
    def add_credit_txn(self, domain_event, process_event):
        self.add_transaction(domain_event.amount, process_event)

    @policy.register(Account.Debited)
    def add_debit_txn(self, domain_event, process_event):
        # note the minus here on domain event amount: subtract debits
        self.add_transaction(-domain_event.amount, process_event)

    def add_transaction(self, amount, process_event):
        try:
            ledger_id = Ledger.create_id(ledger_name)
            ledger = self.repository.get(ledger_id)
        except AggregateNotFound:
            ledger = Ledger(ledger_name)
        ledger.add_transaction(amount)
        process_event.collect_events(ledger)
        #TODO: the logging statement below prints balance and count _before_ the
        #      transaction has been applied - not after.  Even though
        #      ledger.add_transaction() has been called.  Suspect it's to do with
        #      the way the decorator works
        # logging.info(f"ledger updated: balance {self.get_balance()}, {self.get_count()} transactions")

    def get_count(self):
        ledger_id = Ledger.create_id(ledger_name)
        try:
            ledger = self.repository.get(ledger_id)
        except AggregateNotFound:
            return 0
        return ledger.get_transaction_count()

    def get_balance(self):
        ledger_id = Ledger.create_id(ledger_name)
        try:
            ledger = self.repository.get(ledger_id)
        except AggregateNotFound:
            return 0
        return ledger.get_balance()
