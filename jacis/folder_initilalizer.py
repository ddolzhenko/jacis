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

from jacis import utils, core

#-------------------------------------------------------------------------------

class Error(Exception):
    pass

class Stop(Exception):
    pass

#-------------------------------------------------------------------------------

def __init_general(path, structure, forced=False, quiet=False):
    if forced and os.path.exists(path):
        log.debug('removing: ' + root)
        utils.rmdir(root)

    if os.path.exists(root):
        if quiet:
            return
        else:
            raise Stop('{} already exists'.format(path))

    log.debug('creating structure in '+root)
    os.mkdir(path)
    with utils.work_dir(path):
        utils.init_fs_structure(structure)


def init_global(forced=False, quiet=False):
    log.info('initializing jacis global folder')

    structure = yaml.load(  '''
        cache:
            available: {}
            installed:
                list.yml: ""
        config.yml: ""
        ''')

    root = core.jacis_global_dir()
    __init_general(root, structure, forced, quiet)


def init_local(forced=False, quiet=False):
    log.info('initializing jacis local folder')
    structure = yaml.load(  '''
        cache:
            available: {}
            installed:
                list.yml: ""
        config.yml: ""
        ''')

    root = core.jacis_dir()
    __init_general(root, structure, forced, quiet)











