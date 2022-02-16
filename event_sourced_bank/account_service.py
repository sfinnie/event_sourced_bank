from eventsourcing.application import Application
from event_sourced_bank.domain_model import Account


class AccountService(Application):

    def create_account(self):
        ac = Account()
        self.save(ac)
        return ac.id
    
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

        