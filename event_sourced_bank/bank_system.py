from eventsourcing.system import SingleThreadedRunner, System
from event_sourced_bank.account_service import AccountService
from event_sourced_bank.ledger_service import LedgerService
from event_sourced_bank.transaction_log_service import TransactionLogService


class EventSourcedBank:

    def __init__(self):
        self.system = System(pipes=[[AccountService, LedgerService], [AccountService, TransactionLogService]])
        self.runner = SingleThreadedRunner(self.system)

    def start(self):
        self.runner.start()

    def stop(self):
        self.runner.stop()

    def get_account_service(self):
        return self.runner.get(AccountService)

    def get_ledger_service(self):
        return self.runner.get(LedgerService)

    def get_transaction_log_service(self):
        return self.runner.get(TransactionLogService)


