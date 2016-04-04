# Copyright (c) 2016 Dmitry Dolzhenko

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#-------------------------------------------------------------------------------

"""Command line interface tests
"""

#-------------------------------------------------------------------------------

__author__ = "Dmitry Dolzhenko"
__email__  = "d.dolzhenko@gmail.com"

#-------------------------------------------------------------------------------

import os
import unittest
import tempfile
from jacis import utils

#-------------------------------------------------------------------------------

class InternalCommands(unittest.TestCase):
    
    def setUp(self):
        pass
        # utils.work_dir()
        # self.prev_work_dir = os.getcwd()
        # self.work_dir = tempfile.mkdtemp()
        # os.chdir(self.work_dir)

    def tearDown(self):
        pass
        # os.chdir(self.prev_work_dir)
        # utils.rmdir(self.work_dir)

    def cute(self, msg):
        return "{}. CWD: '{}'".format(msg, self.work_dir)

    def assertPredicate(self, p, x, msg=""):
        if not p(x):
            raise AssertionError("{}({}) is false\n : {}".format(p.__name__, x, msg))
    
    def test_full_repo(self):
        
        def prefixed(pref):
            def decorate(f):
                def decorator(*args, **kvargs):
                    print(pref)
                    r = f(*args, **kvargs)
                    print(pref)
                return decorator
            return decorate


        @prefixed("---")
        def foo(a, b):
            print (a)
            print (b)

        a = 2
        b = 3

        foo(a, b)
