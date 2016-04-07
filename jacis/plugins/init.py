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

"""Init subcommand
"""

#-------------------------------------------------------------------------------

__author__ = "Dmitry Dolzhenko"
__email__  = "d.dolzhenko@gmail.com"

#-------------------------------------------------------------------------------

import os, sys
import argparse
import jacis
from jacis import core, utils, config

log = core.get_logger(__name__)

#-------------------------------------------------------------------------------

class Error(Exception):
    def __init__(self, *args):
        super().__init__(*args)


def jacis_plugin(argv):
    try:
        parser = argparse.ArgumentParser(prog='init')
        parser.add_argument('-v', '--verbose',
            action='count', default=0, help='verbose level')
        parser.add_argument('-c', '--clean',
            action='store_true', default=False, help='clean previous one. Kills all previous data')
        args = parser.parse_args(argv)

        # Update logger
        global log
        log = core.get_logger(__name__, args.verbose)


        log.debug("Hi I'm: {} {}".format(__name__, argv))
        log.debug("Parsed args: {}".format(args))

        init(clean=args.clean)

    except Error as e:
        log.error(e)
        sys.exit(1)
    except Exception as e:
        log.critical(e)
        raise

#-------------------------------------------------------------------------------

def init(clean=False):
    from os import mkdir
    from os.path import isdir, join
    from jacis.utils import mktree, rmdir

    home = core.jacis_dir()

    if clean:
        rmdir(home)

    if os.path.isdir(home):
        raise Error("can't init {}. it's already there".format(home))

    mktree(join(home, 'cache'))
    config = jacis.config.Config()
    config.dump_file()


class Test(utils.TestCase):

    def test_1(self):
        jacis_plugin(['-vvvvv', '--clean'])


