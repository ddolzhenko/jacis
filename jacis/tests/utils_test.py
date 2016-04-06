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
from jacis import utils
from jacis.utils import strong_typed

#-------------------------------------------------------------------------------

class TypeDecorators(utils.TestCase):

    def test_static_typed_ok_degenerated(self):
        @strong_typed()
        def test():
            pass
        self.assertEqual(None, test())


    def test_static_typed_ok_trivial(self):
        @strong_typed(returns=str)
        def test():
            return "hello"
        self.assertEqual("hello", test())

        @strong_typed(str) # should return nothing
        def test(a):
            pass
        self.assertEqual(None, test("hello"))

        @strong_typed(str, returns=int)
        def test(a):
            return 42
        self.assertEqual(42, test("hello"))


    def test_static_typed_ok_trivial_2(self):

        @strong_typed(str, str) # should return nothing
        def test(a, b):
            pass
        self.assertEqual(None, test("hello", "world"))

        @strong_typed(str, int) # should return nothing
        def test(a, b):
            pass
        self.assertEqual(None, test("hello", 42))

        @strong_typed(str, str, returns=int)
        def test(a, b):
            return 42
        self.assertEqual(42, test("hello", "world"))

        # @strong_typed(str, str, returns=(int, int))
        # def test(a, b):
        #     return (42, 314)
        # self.assertEqual((42, 314), test("hello", "world"))

    ########################################################
    # NOK

    def test_static_typed_nok_degenerated(self):
        @strong_typed()
        def test():
            return 42
        with self.assertRaises(AssertionError):
            x = test()

    def test_static_typed_nok_trivial(self):
        @strong_typed(returns=int)
        def test():
            pass
        with self.assertRaises(AssertionError):
            x = test()

        @strong_typed(returns=int)
        def test():
            return "hello"
        with self.assertRaises(AssertionError):
            x = test()

        @strong_typed(str) # should return nothing
        def test(a):
            pass
        with self.assertRaises(AssertionError):
            x = test(42)

        # brak both
        @strong_typed(str) # should return nothing
        def test(a):
            return 42
        with self.assertRaises(AssertionError):
            x = test(42)

        # one in one out
        @strong_typed(str, returns=int)
        def test(a):
            return 42
        with self.assertRaises(AssertionError):
            x = test(42)

        @strong_typed(str, returns=int)
        def test(a):
            return "hello"
        with self.assertRaises(AssertionError):
            x = test("hello")

        @strong_typed(str, returns=int)
        def test(a):
            return "hello"
        with self.assertRaises(AssertionError):
            x = test(42)


    def test_static_typed_nok_trivial_2(self):
        @strong_typed(int, int)
        def test(a, b):
            return "hello"
        with self.assertRaises(AssertionError):
            x = test(42, 32)

        @strong_typed(int, int)
        def test(a, b):
            pass
        with self.assertRaises(AssertionError):
            x = test(42, "hello")

        @strong_typed(int, int)
        def test(a, b):
            pass
        with self.assertRaises(AssertionError):
            x = test("hello", 42)
