#!/usr/bin/env python3
# Somehow grade the output based on something.
# This example script do a string compare using `diff -daZB` on each
# test output and reference output.
from utils import *
from sys import argv
from pathlib import Path
with Judging() as e:
	for i in range(0, int(argv[1]) + 1):
		# We do not catch any exceptions, because there is few reasonable
		# way to deal with it.
		# Better pop it up out to the frontend.
		err_path = "/test/err{}".format(i)
		if Path(err_path).exists():
			t = open(err_path)
			# Please consult /run.py on what this err can be
			err=int(t.read().strip(" \n\r"))
			t.close()
			e.add_errored_testcase(err,1)
		else:
			passed = compare_file("/test/{}".format(i), "/judge/tests/output/{}".format(i))
			e.add_boolean_testcase(passed)
