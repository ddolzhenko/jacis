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

"""syncing tool
"""

#-------------------------------------------------------------------------------

__author__ = "Dmitry Dolzhenko"
__email__  = "d.dolzhenko@gmail.com"

#-------------------------------------------------------------------------------

import os
import git
import argparse

#-------------------------------------------------------------------------------

class Error(Exception):
    def __init__(self, *args):
        super().__init__(*args)



def jacis_plugin(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='git url')
    parser.add_argument('dir', help='local dir')

    args = parser.parse_args(argv)

    sync(args.url, args.dir)


def sync(url, local_dir):
    git.Repo.clone_from(url, local_dir)


@utils.strong_typed(str, str, str, str)
def auto_repo(kind, remote_url, remote_dir, local_dir):
    handlers = { 'git', GITRepo }

    if kind not in handlers:
        raise Error('unknown repo: ', kind)

    Repo = handlers[kind]
    return Repo(remote_url, remote_dir, local_dir)



def git_repo(remote_url, remote_dir, local_dir):

    git.Repo(local_dir)


class GITRepo:
    def __init__(self, arg):
        self.arg = arg



