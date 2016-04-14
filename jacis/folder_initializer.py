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

"""Initializes jacis folders
"""

#-------------------------------------------------------------------------------

__author__ = "Dmitry Dolzhenko"
__email__  = "d.dolzhenko@gmail.com"

#-------------------------------------------------------------------------------

import os
import yaml

from jacis import utils, core

log = core.get_logger(__name__)

#-------------------------------------------------------------------------------

class Error(Exception):
    pass

class Error(Exception):
    pass

#-------------------------------------------------------------------------------

def __init_general(path, structure, forced=False, quiet=False):
    if forced and os.path.exists(path):
        log.debug('removing: ' + path)
        utils.rmdir(path)

    if os.path.exists(path):
        if quiet:
            return
        else:
            raise Error('{} already exists'.format(os.path.abspath(path)))

    log.debug('creating structure in '+ path)
    os.mkdir(path)
    utils.init_fs_structure(path, structure)


def init_global(forced=False, quiet=False):
    if not quiet:
        log.info('initializing jacis global folder')

    structure = yaml.load(  '''
        cache:
            available: {}
            installed:
                list.yml: ""
        config.yml: ""
        ''')

    path = core.jacis_global_dir()
    __init_general(path, structure, forced, quiet)


def init_local(forced=False, quiet=False):
    if not quiet:
        log.info('initializing jacis local folder')

    structure = yaml.load(  '''
        cache:
            available: {}
            installed:
                list.yml: ""
        config.yml: ""
        ''')

    path = core.jacis_dir()
    __init_general(path, structure, forced, quiet)











