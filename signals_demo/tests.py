"""
Proof-of-concept tests answering the three AccuKnox interview questions
about Django signals. Run with:

    python manage.py test signals_demo -v 2

Each test class corresponds to one question and prints its conclusion.
"""

import threading
import time

from django.db import transaction
from django.test import TestCase, TransactionTestCase

from .models import Person, SignalLog


class Question1SyncOrAsyncTest(TestCase):
    """QUESTION 1: Are Django signals executed synchronously or
    asynchronously by default?

    ANSWER: Synchronously.
    """

    def test_signal_blocks_the_caller(self):
        start = time.time()
        Person.objects.create(name="Sync Proof")
        elapsed = time.time() - start

        # The receiver sleeps for 2 seconds before returning. If the
        # signal fired asynchronously (e.g. on a background thread or
        # task queue), Person.objects.create() would return almost
        # instantly and `elapsed` would be a tiny fraction of a second.
        # Because we measure >= 2 seconds, the calling code was BLOCKED
        # until the receiver finished -> signals are synchronous.
        self.assertGreaterEqual(elapsed, 2)
        print(f"\n[Q1] create() blocked for {elapsed:.2f}s "
              f"(receiver sleeps for 2s) -> SIGNALS ARE SYNCHRONOUS")


class Question2SameThreadTest(TestCase):
    """QUESTION 2: Do Django signals run in the same thread as the
    caller?

    ANSWER: Yes, by default (unless you explicitly dispatch to another
    thread yourself).
    """

    def test_signal_runs_on_callers_thread(self):
        caller_thread_id = threading.get_ident()

        Person.objects.create(name="Thread Proof")

        log = SignalLog.objects.latest('id')
        receiver_thread_id = int(log.thread_id)

        self.assertEqual(caller_thread_id, receiver_thread_id)
        print(f"\n[Q2] caller thread id={caller_thread_id}, "
              f"receiver thread id={receiver_thread_id} -> SAME THREAD")


class Question3SameTransactionTest(TransactionTestCase):
    """QUESTION 3: Do Django signals run in the same database
    transaction as the caller by default?

    ANSWER: Yes. post_save fires as part of the same atomic block; if
    that block later rolls back, anything the receiver wrote rolls
    back with it.

    We use TransactionTestCase (not TestCase) here specifically
    because TestCase wraps every test in its own outer transaction,
    which would hide real commit/rollback behaviour.
    """

    def test_signal_rolls_back_together_with_caller(self):
        SignalLog.objects.all().delete()
        Person.objects.all().delete()

        with self.assertRaises(RuntimeError):
            with transaction.atomic():
                Person.objects.create(name="Rollback Proof")

                # At this point the post_save receiver has already run
                # and created a SignalLog row -- but we are still
                # inside the same atomic() block that created Person.
                self.assertEqual(SignalLog.objects.count(), 1)

                # Force the entire atomic block to roll back.
                raise RuntimeError("forcing rollback to prove shared transaction")

        # If the signal had run in its OWN separate transaction, the
        # SignalLog row would have already been committed and would
        # still exist here. Instead, both rows vanish -- proving the
        # receiver executed inside the caller's transaction.
        self.assertEqual(Person.objects.count(), 0)
        self.assertEqual(SignalLog.objects.count(), 0)
        print("\n[Q3] Both Person and SignalLog were rolled back together "
              "-> SIGNAL RAN IN THE SAME TRANSACTION AS THE CALLER")
