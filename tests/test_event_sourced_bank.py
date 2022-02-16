from event_sourced_bank.domainmodel import Account
from event_sourced_bank.account_service import AccountService

def test_account_credit_debit():
    ac = Account()
    assert ac.balance == 0
    
    ac.credit(20)
    assert ac.balance == 20

    ac.debit(20)
    assert ac.balance == 0

def test_account_service_credit_debit():
    svc = AccountService()
    account_id = svc.create_account()
    assert svc.get_balance(account_id) == 0

    svc.credit_account(account_id, 30)
    assert svc.get_balance(account_id) == 30

    svc.debit_account(account_id, 20)
    assert svc.get_balance(account_id) == 10


