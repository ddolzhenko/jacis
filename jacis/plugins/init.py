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
from jacis import core, utils, folder_initializer

log = core.get_logger(__name__)

#-------------------------------------------------------------------------------

def jacis_plugin(argv):
    try:
        parser = argparse.ArgumentParser(prog='init')
        parser.add_argument('-v', '--verbose',
            action='count', default=0, help='verbose level')
        parser.add_argument('-f', '--forced',
            action='store_true', default=False, help='clean previous one. Kills all previous data')
        parser.add_argument('-g', '--global',
            action='store_true', default=False, help='affects global folder only')
        args = parser.parse_args(argv)

        core.set_log_verbosity(args.verbose)

        log.debug("Hi I'm: {} {}".format(__name__, argv))
        log.debug("Parsed args: {}".format(args))

        init(glob=vars(args)['global'], forced=args.forced)
    except folder_initializer.Error as e:
        log.error(e)


#-------------------------------------------------------------------------------

def init(glob, forced):
    if glob:
        folder_initializer.init_global(forced=forced)
    else:
        folder_initializer.init_global(forced=forced, quiet=True)
        folder_initializer.init_local(forced=forced)


class Test(utils.TestCase):
    def test_1(self):
        with utils.work_dir('d:\\src\\repos\jacis\\.temp'):
            # jacis_plugin(['-vvv', '-f'])
            jacis_plugin(['-vv', '-f'])