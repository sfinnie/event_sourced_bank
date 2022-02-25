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
        logging.debug(f"domain event: type '{type(domain_event)}', value {domain_event}")
        event = self.transaction_log.trigger_event(account_id=domain_event.originator_id,
                                                   transaction_type="Credit",
                                                   amount=domain_event.amount)
        logging.info(f"logged event: {event}")
        self.save(event)

    def get_transactions(self):
        txns = [{"id": txn.account_id,
                 "amount": txn.amount,
                 "type": txn.transaction_type} for txn in self.transaction_log.get()]
        return txns
