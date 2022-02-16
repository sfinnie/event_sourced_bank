from event_sourced_bank.domainmodel import Account
from event_sourced_bank.account_service import AccountService

def test_account_credit_debit():
    ac = Account()
    assert ac.balance == 0
    
    ac.credit(20)
    assert ac.balance == 20

    ac.debit(20)
    assert ac.balance == 0

def test_bank_credit_debit():
    bank = AccountService()
    account_id = bank.create_account()
    assert bank.get_balance(account_id) == 0

    bank.credit_account(account_id, 30)
    assert bank.get_balance(account_id) == 30

    bank.debit_account(account_id, 20)
    assert bank.get_balance(account_id) == 10


