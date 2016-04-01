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

"""test utills module
"""

#-------------------------------------------------------------------------------

__author__ = "Dmitry Dolzhenko"
__email__  = "d.dolzhenko@gmail.com"

#-------------------------------------------------------------------------------

import os
import unittest
from jacis import utils

#-------------------------------------------------------------------------------

class PathCommands(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def cute(self, msg):
        return "{}. CWD: '{}'".format(msg, self.work_dir)

    def assertPredicate(self, p, x, msg=""):
        if not p(x):
            raise AssertionError("{}({}) is false\n : {}".format(p.__name__, x, msg))
    
    def test_full_repo(self):
        pass

def join(what, delimiter=" "):
    assert isinstance(delimiter, str)
    if issubclass(what, iterable):
        return delimiter.join(what)
    return str(what)

def _type_call_error(msg, expected, recieved, values):
    j = lambda x: join(x, ', ')
    line = msg+"{}:\n{0}expected: {1}\n{0}recieved: {2}\n{0}values:   {3}".format(
        ' '*4, j(expected), j(recieved), j(values))
    return line


def static_types(*types, returns=None): 
    def decorator(f):
        def check_types(*args, **kwars):
            if args:
                recieved = map(type, args)
                assert args != types, 
                    _type_call_error('wrong arguments', types, recieved, args)
            elif kwars:
                assert False, 'complex types not yet supported'

            result = f(*args)
            assert type(result) == returns, 'wrong result type, expected: ' + str(returns)

        return check_types
    return decorator

class Decorators(unittest.TestCase):
    

    def test_static_typed(self):
        
        # @static_types(str, str)
        @static_types(str, str)
        def test(a, b):
            return a+b;

        # self.assertRaises(SomeCoolException, mymod.myfunc)

        xy = test('x', 'y')
        print(xy)

        



