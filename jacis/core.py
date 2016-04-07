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
import logging

from jacis import utils

#-------------------------------------------------------------------------------

def __setup_root_logger(name):
    # create logger
    logger = logging.getLogger(name)
    # logger.setLevel(logging.WARNING)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    # ch.setLevel(logging.WARNING)

    # create formatter
    formatter = logging.Formatter('%(name)s>>%(levelname)8s: %(message)s')
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    return logger

__root_logger = __setup_root_logger('jacis')

def get_logger(name, verbosity=0):
    logger = logging.getLogger(name)
    if verbosity>= 2:
        logger.setLevel(logging.DEBUG)
    elif verbosity== 1:
        logger.setLevel(logging.INFO)
    elif verbosity== 0:
        logger.setLevel(logging.WARNING)
    else:
        assert verbosity>= 0, 'invalid logger verbosity'
    return logger

__self_path = os.path.dirname(__file__)
def get_self_path():
    return __self_path

###############################################################################
# dir

def jacis_dir():
    j = '.jacis'
    return j

def jacis_global_dir():
    j = '.jacis'
    return os.path.join(utils.home_dir(), j)

###############################################################################
# plugins and tests

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

