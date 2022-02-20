# Run a sample of transactions through a bank
from event_sourced_bank.account_service import AccountService
from event_sourced_bank.bank_system import EventSourcedBank
import logging
logging.basicConfig(level=logging.INFO)


logging.info("Starting the bank")
bank = EventSourcedBank()
bank.start()

account_svc = bank.get_account_service()
ledger_svc = bank.get_ledger_service()

ac1 = account_svc.create_account()
account_svc.credit_account(ac1, 20)
account_svc.credit_account(ac1, 20)
account_svc.credit_account(ac1, 20)
account_svc.debit_account(ac1, 40)
assert ledger_svc.get_balance() == 20

ac2 = account_svc.create_account()
account_svc.credit_account(ac2, 42)
account_svc.debit_account(ac2, 12)
assert ledger_svc.get_balance() == 50

account_ids = account_svc.get_all_account_ids()
logging.info(f"bank has {len(account_ids)} accounts")

logging.info(f"ledger status: balance {ledger_svc.get_balance()}, {ledger_svc.get_count()} transactions")
