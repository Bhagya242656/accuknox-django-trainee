import threading
import time

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Person, SignalLog


@receiver(post_save, sender=Person)
def person_post_save_handler(sender, instance, created, **kwargs):
    """
    Fires every time a Person is saved.

    Three things happen here, each aimed at one of the three questions:

    1. We sleep for 2 seconds. If signals were asynchronous, the code
       that triggered the save (see tests.py) would NOT block waiting
       for this to finish.

    2. We record threading.get_ident() into SignalLog. If this matches
       the thread id captured by the calling code, the signal ran on
       the same thread.

    3. We create a SignalLog row using the *default* database connection,
       with no explicit transaction handling of our own. If the caller
       wraps the save in transaction.atomic() and then raises an
       exception, this row will only survive if it was NOT part of the
       same transaction as the caller.
    """
    if not created:
        return

    thread_id = threading.get_ident()

    # --- Question 1: sync vs async -----------------------------------
    time.sleep(2)

    # --- Question 2 & 3: thread id + transaction membership ----------
    SignalLog.objects.create(
        thread_id=str(thread_id),
        message=f"post_save fired for Person(name={instance.name!r})",
    )
