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

"""Plugin loader
"""

#-------------------------------------------------------------------------------

__author__ = "Dmitry Dolzhenko"
__email__  = "d.dolzhenko@gmail.com"

#-------------------------------------------------------------------------------

import os
import inspect
import unittest
import glob
import importlib

#-------------------------------------------------------------------------------

__self_path = os.path.dirname(__file__)

def get_self_path():
    return __self_path

from jacis.plugins import *
def get_plugins():
    from jacis import plugins
    members = (x for x in inspect.getmembers(plugins))
    modules = (x for x in members if inspect.ismodule(x[1]))
    plugins = (x for x in modules if hasattr(x[1], "jacis_plugin"))
    return dict(plugins)

def get_test_module_names():
    mask = '**/*_test.py'
    for filename in glob.iglob(mask, recursive=True):
        name = os.path.splitext(filename)[0]
        module_name = name.replace('\\', '.').replace('/', '.')
        yield module_name

def get_tests():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    for module_name in get_test_module_names():
        module = importlib.import_module(module_name)
        tests = loader.loadTestsFromModule(module)
        suite.addTests(tests)

    return suite

