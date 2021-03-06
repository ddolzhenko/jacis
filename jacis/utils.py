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

"""Utilities (that should be in python)
"""

#-------------------------------------------------------------------------------

__author__ = "Dmitry Dolzhenko"
__email__  = "d.dolzhenko@gmail.com"

#-------------------------------------------------------------------------------

import os
import subprocess
import checksumdir
import shutil
import stat
import unittest
import collections
import tempfile

#-------------------------------------------------------------------------------
# tests

class TestCase(unittest.TestCase):

    def assertPredicate(self, p, x, msg=""):
        if not p(x):
            raise AssertionError("{}({}) is false\n : {}".format(p.__name__, x, msg))


#-------------------------------------------------------------------------------
# modules

def get_module_names(init_file):
    import glob
    from os.path import dirname, basename, isfile, splitext
    pys = glob.glob(dirname(init_file) + "/*.py")
    return [splitext(basename(py))[0] for py in pys if isfile(py)]

def get_public_module_names(init_file):
    return [x for x in get_module_names(init_file) if not x.startswith('_')]

#-------------------------------------------------------------------------------
# types:

def _type_call_error(msg, expected, recieved, values):
    j = lambda x: join(x, ', ')
    line = msg+":\n{0}expected: {1}\n{0}recieved: {2}\n{0}values:   {3}".format(' '*4, j(expected), j(recieved), j(values))
    return line


def strong_typed(*expected_types, returns=type(None)):
    def decorator(f):
        def check_types(*args, **kvargs):
            if args:
                recieved = map(type, args)
                ok = all(map(lambda p: p[0]==p[1], zip(recieved, expected_types)))
                assert ok, _type_call_error('wrong arguments', expected_types, recieved, args)
            elif kvargs:
                assert False, 'complex types not yet supported'

            result = f(*args, **kvargs)
            assert type(result) == returns, 'wrong result type, expected: {}, recieved: {}'.format(returns, type(result))

            return result

        return check_types
    return decorator

#-------------------------------------------------------------------------------
# string utils

def join(what, delimiter=" "):
    assert isinstance(delimiter, str)
    if isinstance(what,  collections.Iterable):
        return delimiter.join(map(str, what))
    return str(what)

#-------------------------------------------------------------------------------
# system

def im_on_windows():
    return os.name == 'nt'

#-------------------------------------------------------------------------------
# folders

def init_fs_structure(path, structure):
    '''Creates folder structure in path according dict from parameters
    example:
    istream = open('filename.txt')
    structure = {
        folder_l0_1: {                   #this is a folder because dict inside
            folder_l1_1 : {},            #this is a empty folder inside upper folder
            file_l1_1.txt: 'Hello world!',   #this is file with contents 'Hello world'
            file_l1_2.ext: istream             #this will create a file with contents from file stream
        },
        file_l0_1: some text inside # file on top
    }

    init_fs_structure(structure)
    '''
    assert isinstance(structure, dict)
    with work_dir(path):
        for name, data in structure.items():
            assert data is not None
            if isinstance(data, dict):  # create a folder
                os.mkdir(name)
                init_fs_structure(name, data)
            elif isinstance(data, str): # just a file
                with open(name, 'w') as f:
                    f.write(data)
            else:                       # everything else threated as stream
                with open(name, 'w') as f:
                    f.write(data.read())



def home_dir():
    if im_on_windows():
        return os.environ['USERPROFILE']

    return os.path.expanduser('~')

def checksum(path):
    """Directory sha1 checksum"""
    return checksumdir.dirhash(path, 'sha1')

def split_path_all(path):
    norm = os.path.normpath(path)
    return norm.split(os.sep)

def mktree(path):
    '''Creates not only last folder in path but all
    for mktree('1/2/3')
    will create 1/
                1/2
                1/2/3
    '''
    folders = split_path_all(path)
    for i, folder in enumerate(folders):
        f = os.sep.join(folders[:i+1])
        if not os.path.isdir(f):
            os.mkdir(f)


def rmdir(path):
    """Forced directory remove"""
    def onerror(func, path, exc_info):
        if not os.access(path, os.W_OK):
            os.chmod(path, stat.S_IWUSR)
            func(path)
        else:
            raise

    shutil.rmtree(path, onerror=onerror)


class work_dir(object):
    """change working dir within 'with' context
    Usage:
        with workdir('otherdir/foo/'):
            print(os.getcwd())
        print(os.getcwd()) # oldone
    """
    def __init__(self, directory):
        assert isinstance(directory, str)
        self._current  = os.getcwd()
        self._previous = os.getcwd()
        self._wanted = directory

    @property
    def previous(self):
        return self._previous

    @property
    def current(self):
        return self._current

    def __enter__(self):
        self._previous = os.getcwd()
        os.chdir(self._wanted)
        self._current = os.getcwd()
        return self

    def __exit__(self, *args):
        os.chdir(self._previous)
        self._current = os.getcwd()

    def __str__(self):
        return self.current


class temp_work_dir:

    def __enter__(self):
        self._work_dir = work_dir(tempfile.mkdtemp())
        self._work_dir.__enter__()

    def __exit__(self, *args):
        tmp = self._work_dir.current
        self._work_dir.__exit__()
        rmdir(tmp)
        self._work_dir = None

    def __str__(self):
        return str(self._work_dir)


def system_call(*args, timeout=10):
    return subprocess.run(args, timeout=timeout)

