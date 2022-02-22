import logging
from typing import Optional, List, Dict, Tuple
from uuid import UUID

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from event_sourced_bank.bank_system import EventSourcedBank

logging.basicConfig(level=logging.INFO)

# Set up the web server environment
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ...and start the bank system
bank = EventSourcedBank()
bank.start()
account_svc = bank.get_account_service()
ledger_svc = bank.get_ledger_service()


def get_bank_state() -> Tuple:
    ac_ids = account_svc.get_all_account_ids()
    accounts = [{"index": idx, "id": id, "balance": account_svc.get_balance(id)} for idx, id in enumerate(ac_ids)]
    balance = ledger_svc.get_balance()
    transaction_count = ledger_svc.get_transaction_count()
    return accounts, balance, transaction_count


def render_bank_state(request: Request, template="bank_state.html"):
    # import time
    # time.sleep(3.0)
    accounts, balance, transaction_count = get_bank_state()
    return templates.TemplateResponse(template,
                                      {"request": request,
                                       "accounts": accounts,
                                       "balance": balance,
                                       "transaction_count": transaction_count})


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return render_bank_state(request, "index.html")


@app.post("/create-account", response_class=HTMLResponse)
def create_account(request: Request):
    account_svc.create_account()
    return render_bank_state(request)


@app.post("/credit-account", response_class=HTMLResponse)
def credit_account(request: Request,
                   account: str = Form(""),
                   amount: int = Form(0)):
    account_svc.credit_account(UUID(account), amount)
    return render_bank_state(request)


@app.post("/debit-account", response_class=HTMLResponse)
def debit_account(request: Request,
                   account: str = Form(""),
                   amount: int = Form(0)):
    account_svc.debit_account(UUID(account), amount)
    return render_bank_state(request)


if __name__ == "__main__":
    logging.info("opening the bank")
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
    bank.stop()
    logging.info("bank closed")
