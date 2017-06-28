from functools import wraps
import logging
import time

from .errors import LockWaitTimeoutError, LockDeadlockError


def retry_on_lock(max_retries=3, wait_time=5, exception_classes=(LockDeadlockError, LockWaitTimeoutError), log_func=None):
    """
    Function wrapper to allow retries when writing to the database when any of the exception classes are encountered.

    :param max_retries: The maximum number of times to retry before re-raising the original error.
    :param wait_time: The time to wait before attempting to retry.
    :param exception_classes: A tuple of exception classes to retry when encountered.
    :param log_func: Callable object which is called when error is encountered. Default is logging.debug.
        Exception instance will be passed as a single parameter to the callable.
    :return:
    """
    log_func = log_func or logging.debug
    def wrapped(f):
        @wraps(f)
        def inner(*args, **kwargs):
            tries = 0
            while True:
                try:
                    return f(*args, **kwargs)
                except exception_classes as e:
                    log_func(e)
                    time.sleep(wait_time)
                    tries += 1
                    if tries == max_retries:
                        raise
        return inner
    return wrapped
