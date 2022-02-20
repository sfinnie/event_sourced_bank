from typing import List
from uuid import UUID

from eventsourcing.application import Application
from event_sourced_bank.domain_model import Account


class AccountService(Application):
    # see discussion on snapshots in [readme](../readme.md#snapshots)
    snapshotting_intervals = {Account: 50}
    # list of all accounts
    account_ids: List[UUID] = []

    def create_account(self):
        ac = Account()
        self.save(ac)
        AccountService.account_ids.append(ac.id)
        return ac.id

    @classmethod
    def get_all_account_ids(cls) -> List[UUID]:
        return AccountService.account_ids

    def get_balance(self, account_id) -> int:
        ac = self.repository.get(account_id)
        return ac.balance
    
    def credit_account(self, account_id, amount: int):
        ac = self.repository.get(account_id)
        ac.credit(amount)
        self.save(ac)
    
    def debit_account(self, account_id, amount: int):
        ac = self.repository.get(account_id)
        ac.debit(amount)
        self.save(ac)

        