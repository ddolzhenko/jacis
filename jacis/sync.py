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

"""syncing tools
"""

#-------------------------------------------------------------------------------

__author__ = "Dmitry Dolzhenko"
__email__  = "d.dolzhenko@gmail.com"

#-------------------------------------------------------------------------------

import os
import git
import svn.remote
from urllib.parse import urljoin

from jacis import core, utils

#-------------------------------------------------------------------------------

log = core.get_logger(__name__)

#-------------------------------------------------------------------------------

class Error(Exception):
    pass

#-------------------------------------------------------------------------------


def git_clone(url, path, tag=None):
    log.debug('git clone {} {}'.format(url, path))
    repo = git.Repo.clone_from(url, path)
    if tag:
        tag_path = 'tags/{}'.format(tag)
        log.debug('git checkout: '+tag_path)
        res = repo.git.checkout(tag_path)
        print(res)


def svn_clone(url, path, tag=None):
    r = svn.remote.RemoteClient(url)
    if tag:
        path = urljoin(path, tag)
    r.checkout(path)


def store(info, **kvargs):
    path = kvargs['path']

    who = info['type']
    url = info['url']
    tag = info['tag']

    if who == 'git':
        git_clone(url, path, tag)
    elif who == 'svn':
        svn_clone(url, path, tag)
    else:
        raise Exception('not supported: ' + who)

