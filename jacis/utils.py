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
import checksumdir
import shutil
import stat

#-------------------------------------------------------------------------------


def checksum(path):
    """Directory sha1 checksum"""
    return checksumdir.dirhash(path, 'sha1')


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
        cwd = os.getcwd()
        self.current  = cwd
        self.previous = cwd

        self._wanted = directory

    def __enter__(self):
        self.previous = self.current
        os.chdir(self._wanted)
        self.current = os.getcwd()
        return self

    def __exit__(self, *args):
        os.chdir(self.previous)
        self.current = self.previous

