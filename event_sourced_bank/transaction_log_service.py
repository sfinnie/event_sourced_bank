from uuid import UUID, uuid5, NAMESPACE_URL

from eventsourcing.application import AggregateNotFound
from eventsourcing.system import ProcessApplication
from eventsourcing.dispatch import singledispatchmethod
from event_sourced_bank.domain_model import Account, Ledger
from eventsourcing.application import EventSourcedLog, LogEvent

import logging


class AccountEvent(LogEvent):
    account_id: UUID
    transaction_type: str
    amount: int = 0


class TransactionLogService(ProcessApplication):

    def __init__(self, env=None) -> None:
        super().__init__(env=env)
        self.aggregate_log = EventSourcedLog(
            events=self.events,
            originator_id=uuid5(NAMESPACE_URL, "/transactions"),
            logged_cls=AccountEvent,
        )

    @singledispatchmethod
    def policy(self, domain_event, process_event):
        """Default policy"""

    @policy.register(Account.Credited)
    def add_credit_txn(self, domain_event, process_event) -> None:
        logging.info(f"domain event: type '{type(domain_event)}', value {domain_event}")
        logging.info(f"process event: type '{type(process_event)}', value {process_event}")
        logged_id = self.aggregate_log.trigger_event(account_id=domain_event.originator_id,
                                                     transaction_type=type(domain_event).__name__,
                                                     amount=domain_event.amount)
        logging.info(f"logged_id: {logged_id}")
        self.save(logged_id)
