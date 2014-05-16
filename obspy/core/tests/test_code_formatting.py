# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.builtins import *  # NOQA

import inspect
from obspy.core.util.decorator import skipIf
from obspy.core.util.testing import check_flake8
import os
import re
import unittest


class CodeFormattingTestCase(unittest.TestCase):
    """
    Test codebase for compliance with the flake8 tool.
    """

    @skipIf('OBSPY_NO_FLAKE8' in os.environ, 'flake8 check disabled')
    def test_flake8(self):
        """
        Test codebase for compliance with the flake8 tool.
        """
        report, message = check_flake8()
        file_count = report.counters["files"]
        error_count = report.get_count()
        self.assertTrue(file_count > 10)
        self.assertEqual(error_count, 0, message)


class FutureUsageTestCase(unittest.TestCase):
    def test_future_imports_in_every_file(self):
        """
        Tests that every single Python file includes the appropriate future
        headers to enforce consistent behaviour.
        """
        test_dir = os.path.abspath(inspect.getfile(inspect.currentframe()))
        obspy_dir = os.path.dirname(os.path.dirname(os.path.dirname(test_dir)))

        future_import_line = (
            "from __future__ import (absolute_import, division, "
            "print_function, unicode_literals)")
        builtins_line = "from future.builtins import *  # NOQA"

        future_imports_pattern = re.compile(
            r"^from __future__ import \(absolute_import,\s*"
            r"division,\s*print_function,\s*unicode_literals\)$",
            flags=re.MULTILINE)

        builtin_pattern = re.compile(
            r"^from future\.builtins import \*  # NOQA$",
            flags=re.MULTILINE)

        failures = []
        # Walk the obspy directory.
        for dirpath, _, filenames in os.walk(obspy_dir):
            # Find all Python files.
            filenames = [os.path.abspath(os.path.join(dirpath, i)) for i in
                         filenames if i.endswith(".py")]
            for filename in filenames:
                with open(filename, "rt") as fh:
                    content = fh.read()

                    if re.search(future_imports_pattern, content) is None:
                        failures.append("File '%s' misses imports: %s" %
                                        (filename, future_import_line))

                    if re.search(builtin_pattern, content) is None:
                        failures.append("File '%s' misses imports: %s" %
                                        (filename, builtins_line))
        self.assertEqual(len(failures), 0, "\n" + "\n".join(failures))


def suite():

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CodeFormattingTestCase, 'test'))
    suite.addTest(unittest.makeSuite(FutureUsageTestCase, 'test'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
