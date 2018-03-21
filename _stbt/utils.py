import errno
import os
import tempfile
from contextlib import contextmanager
from shutil import rmtree


def mkdir_p(d):
    """Python 3.2 has an optional argument to os.makedirs called exist_ok.  To
    support older versions of python we can't use this and need to catch
    exceptions"""
    try:
        os.makedirs(d)
    except OSError, e:
        if e.errno == errno.EEXIST and os.path.isdir(d) \
                and os.access(d, os.R_OK | os.W_OK):
            return
        else:
            raise


@contextmanager
def named_temporary_directory(
        suffix='', prefix='tmp', dir=None):  # pylint: disable=W0622
    dirname = tempfile.mkdtemp(suffix, prefix, dir)
    try:
        yield dirname
    finally:
        rmtree(dirname)


@contextmanager
def scoped_curdir():
    with named_temporary_directory() as tmpdir:
        olddir = os.path.abspath(os.curdir)
        os.chdir(tmpdir)
        try:
            yield olddir
        finally:
            os.chdir(olddir)


def sleep_until(target, _time=None):
    """
    :param target: Time to sleep until, in unix format (seconds since epoch).
    :param _time: For mocking in unit-tests.
    """

    if _time is None:
        import time as _time

    # `sleep` is inside a `while` loop because the actual suspension
    # time of `sleep` may be less than that requested.
    while True:
        seconds_to_wait = target - _time.time()
        if seconds_to_wait > 0:
            _time.sleep(seconds_to_wait)
        else:
            return
