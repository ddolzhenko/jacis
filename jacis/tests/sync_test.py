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

"""sync module test
"""

#-------------------------------------------------------------------------------

__author__ = "Dmitry Dolzhenko"
__email__  = "d.dolzhenko@gmail.com"

#-------------------------------------------------------------------------------

import os
import unittest
import tempfile
from jacis import sync, utils

#-------------------------------------------------------------------------------

class BaseTestCase(unittest.TestCase):
    
    def setUp(self):
        self.prev_work_dir = os.getcwd()
        self.work_dir = tempfile.mkdtemp()
        os.chdir(self.work_dir)

        self.repos = {
            "https://github.com/ddolzhenko/TestGit.git" : dict(name="git-http", hash="aaea772d08e46f700797a79615bb566b1254b48b"),
            }

    def tearDown(self):
        os.chdir(self.prev_work_dir)
        utils.rmdir(self.work_dir)

    def cute(self, msg):
        return "{}. CWD: '{}'".format(msg, self.work_dir)

    def assertPredicate(self, p, x, msg=""):
        if not p(x):
            raise AssertionError("{}({}) is false\n : {}".format(p.__name__, x, msg))
    
    def test_full_repo(self):
        for url, data in self.repos.items():
            repo = data["name"]
            sync.sync(url, repo)

            with self.subTest(url=url):
                self.assertPredicate(os.path.isdir, repo, self.cute("not a folder"))
                with utils.work_dir(repo):
                    self.assertEqual(utils.checksum('test'), data["hash"], self.cute('folder checksum failed'))
