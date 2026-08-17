# AccuKnox Django Trainee — Technical Round Submission

This project answers the three Django Signals questions with runnable,
assertion-based proof, and includes a `Rectangle` class exercise.

## Setup

```bash
python -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
```

## Part 1 — Django Signals

All proof is in `signals_demo/tests.py`. Run it with:

```bash
python manage.py test signals_demo -v 2
```

### Question 1: Are Django signals synchronous or asynchronous by default?
**Answer: Synchronous.**
The `post_save` receiver in `signals_demo/signals.py` sleeps for 2 seconds.
`Question1SyncOrAsyncTest` times `Person.objects.create(...)` and asserts
the call takes at least 2 seconds — proving the caller blocks until the
receiver finishes.

### Question 2: Do signals run in the same thread as the caller?
**Answer: Yes.**
The receiver records `threading.get_ident()` into a `SignalLog` row.
`Question2SameThreadTest` compares that to the thread id captured in the
test itself and asserts they're equal.

### Question 3: Do signals run in the same DB transaction as the caller?
**Answer: Yes, by default.**
`Question3SameTransactionTest` wraps a `Person.objects.create(...)` call
in `transaction.atomic()`, then deliberately raises an exception to force
a rollback. Because the `SignalLog` row created *inside* the receiver
also disappears, the receiver must have executed inside the same
transaction as the caller. (Uses `TransactionTestCase`, not `TestCase`,
so the rollback behaviour isn't masked by Django's per-test transaction
wrapping.)

## Part 2 — Rectangle class

See `python_exercises/rectangle.py`. Run tests with:

```bash
python -m unittest python_exercises.test_rectangle -v
```

`Rectangle(length, width)` is iterable and yields `{'length': ...}`
followed by `{'width': ...}`.
