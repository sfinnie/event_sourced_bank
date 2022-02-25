from uuid import UUID, uuid5, NAMESPACE_URL

from eventsourcing.system import ProcessApplication
from eventsourcing.dispatch import singledispatchmethod
from event_sourced_bank.domain_model import Account
from eventsourcing.application import EventSourcedLog, LogEvent

import logging


class AccountEvent(LogEvent):
    account_id: UUID
    transaction_type: str
    amount: int = 0


class TransactionLogService(ProcessApplication):

    def __init__(self, env=None) -> None:
        super().__init__(env=env)
        self.transaction_log = EventSourcedLog(
            events=self.events,
            originator_id=uuid5(NAMESPACE_URL, "/transactions"),
            logged_cls=AccountEvent,
        )

    @singledispatchmethod
    def policy(self, domain_event, process_event):
        """Default policy"""

    @policy.register(Account.Credited)
    def add_credit_txn(self, domain_event, process_event) -> None:
        # logging.info(f"domain event: type '{type(domain_event)}', value {domain_event}")
        # TODO: this isn't logging the Account ID, it's the event ID.
        event = self.transaction_log.trigger_event(account_id=domain_event.originator_id,
                                                   transaction_type=type(domain_event).__name__,
                                                   amount=domain_event.amount)
        logging.info(f"logged event: {event}")
        self.save(event)
