from django.db import models


class Person(models.Model):
    """A trivial model. Saving a Person is what triggers our post_save
    signal, which the tests use to answer Questions 1-3."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SignalLog(models.Model):
    """Written to *inside* the signal receiver itself. Because this row
    is created by the receiver (not by the test), whatever happens to
    it (does it persist? which thread wrote it? when?) tells us
    everything about how the signal executed relative to the caller.
    """
    thread_id = models.CharField(max_length=100, blank=True, null=True)
    triggered_at = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.message
