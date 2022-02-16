# Event Sourced Bank

A "wide but shallow" example of using the Python [event sourcing library](https://github.com/pyeventsourcing/eventsourcing).  "Wide" in the sense that it covers most features in the library; "shallow" in the sense that the use of each is trivial.  It's purpose is not to be an authentic bank: it's to demonstrate the various library components in an example where the domain model itself affords no learning curve.

## Overview

The domain model is simple. It comprises only 2 classes, both in the [domain model](event_sourced_bank/domain_model.py) file.  `Account` models a trivial bank account as an event-sourced [Domain-Driven Design](https://en.wikipedia.org/wiki/Domain-driven_design) Aggregate.  `Ledger` is an equally simple abstraction of a ledger, again modelled as a DDD Aggregate.  

The idea is that all transactions on all accounts get recorded in the ledger:  

* Each transaction on each account generates an event;
* The ledger listens to those events, and is updated accordingly.

## Implementation

The `Account` and `Ledger` aggregates are implemented using the `eventsourcing` library's [Aggregate](https://eventsourcing.readthedocs.io/en/latest/topics/domain.html) base class.

Each aggregate is wrapped in a service.  The [AccountService](event_sourced_bank/account_service.py) uses the `eventsourcing` library's [Application](https://eventsourcing.readthedocs.io/en/latest/topics/application.html) class, and provides an API for creating/retrieving accounts and then acting on them.  The [LedgerService](event_sourced_bank/ledger_service.py) is implemented using the library's [ProcessApplication](https://eventsourcing.readthedocs.io/en/latest/topics/system.html).  Its purpose is to follow all transactions on all accounts, so a single ledger tracks the overall balance in the bank.

The [EventSourcedBank](event_sourced_bank/bank_system.py) class ties everything together.  It wires the `AccountService` and `LedgerService` together, so transactions on `Accounts` are recorded in the `Ledger`.  There's a minimal [main](main.py) that creates a system and runs a few transactions through. 

## Installation

1. Clone this repo:

        $ cd /my/projects/dir
        $ git clone https://github.com/sfinnie/event_sourced_bank.git
        $ cd event_sourced_bank

2. (optional but recommended): create a virtual environment:

        $ python3 -m venv venv
        $ source venv/bin/activate

3. Install dependencies

        $ python3 -m pip install -U pip
        $ python3 -m pip install eventsourcing pytest

## Running

There's a minimal, trivial, script to run the app:

    $ python3 main.py

## Testing

There are a few tests, more as examples than a comprehensive test suite at the moment.  To be enhanced.  To run:

    $ pytest

