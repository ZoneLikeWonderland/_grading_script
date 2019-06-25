import sys
from sys import __stdin__ as stdin

import subprocess

# These are various error code you can use in add_errored_testcase
ERROR_CPU_TIME_LIMIT_EXCEEDED = 1
ERROR_REAL_TIME_LIMIT_EXCEEDED = 2
ERROR_MEMORY_LIMIT_EXCEEDED = 3
ERROR_RUNTIME_ERROR = 4
ERROR_SYSTEM_ERROR = 5
ERROR_UNKNOWN = 6


def compare_file(lhs, rhs, ignore_blank_line=True):
    """
    Compare two files in text mode. Accepts file names or `sys.__stdin__` only.
    If stdin is given, it will be read until EOF.

    Under the hood `diff -aZB` is used, which means `a\n\n\na` and `a\na`
    is identical! If you wish to stress this difference you should pass
    `ignore_blank_line=False`, which will change the underlying command
    to `diff -a`.

    :return bool:
    """
    opt = "-qa"
    if ignore_blank_line:
        opt += "ZB"

    if lhs == stdin:
        if not isinstance(rhs, str):
            raise TypeError("rhs is of type %s while str is expected" % type(rhs))
        a, b = "-", rhs
    elif rhs == stdin:
        if not isinstance(lhs, str):
            raise TypeError("lhs is of type %s while str is expected" % type(rhs))
        a, b = "-", lhs
    else:
        if not isinstance(lhs, str):
            raise TypeError("lhs is of type %s while str is expected" % type(rhs))
        if not isinstance(rhs, str):
            raise TypeError("rhs is of type %s while str is expected" % type(rhs))
    a, b = lhs, rhs
    ret = subprocess.run(args=["/usr/bin/diff", opt, a, b], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return not ret.returncode


def compare_str(lhs: str, rhs: str):
    """
    Compare two strings, with ending spaces and line break striped on
    both side.
    :return bool:
    """
    # tab is left out as it does not seems to be natural
    return lhs.rstrip(" \n\r") == rhs.rstrip(" \n\r")


# TODO RMSE

class Judging(object):
    """
    This class is intended to be used in this manner:

        with Judging() as e:
            e.add_boolean_testcase(compare(input(), "reference output 1"))
            e.add_boolean_testcase(compare(input(), "reference output 2"))
            e.add_boolean_testcase(compare(input(), "reference output 3"))
            # ...
            e.add_scored_testcase(rmse(input(), GroundTruth()), 100)s
            # ...
    """

    def __init__(self):
        self.reports = []

    def __enter__(self):
        return self

    def err(self, *args):
        print(*args, file=sys.stderr)

    def add_errored_testcase(self, error_code, max_credit, index=None):
        """
        Report a test case has failed. Passing anything else than those
        defined in this module will result it to be coerced into ERROR_UNKNOWN.

        """
        if error_code > 6 or error_code < 1:
            self.err("Unknown error code %d, treating as ERROR_UNKNOWN!" % error_code)
            error_code = 6
        self.reports.append((len(self.reports) if index is None else index, 0, max_credit, error_code))

    def add_scored_testcase(self, awarded_credit, max_credit, index=None):
        """
        Report a testcase which give full credit or give 0 credit
        :param int awarded_credit: How much credit the student should
        be awarded
        :param int max_credit: The max credit a student can get from
        this test case.
        :param int index: The index of this testcase. Leave None to
        use a serial number beginning from 0, incrementing on every
        testcase reported (increase even if a testcase has an explicit
        index
        """
        self._add_testcase(awarded_credit, max_credit, index)

    def add_boolean_testcase(self, passed, max_credit=1, index=None):
        """
        Report a testcase which give full credit or give 0 credit
        :param bool passed: Whether student should be awarded the credit
        :param int max_credit: The max credit a student can get from
        this test case.
        :param int index: The index of this testcase. Leave None to
        use a serial number beginning from 0, incrementing on every
        testcase reported (increase even if a testcase has an explicit
        index
        """
        self._add_testcase(max_credit if passed else 0, max_credit, index)

    def _add_testcase(self, score, max_score, index):
        self.reports.append((len(self.reports) if index is None else index, score, max_score, 0))

    def __exit__(self, exc_type, exc_val, exc_tb):
        for r in self.reports:
            print(*r, sep=',')
