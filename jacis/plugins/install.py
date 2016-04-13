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

"""Install package
"""

#-------------------------------------------------------------------------------

__author__ = "Dmitry Dolzhenko"
__email__  = "d.dolzhenko@gmail.com"

#-------------------------------------------------------------------------------

import os, uuid, argparse

import jacis
from jacis import core, utils, packages

log = core.get_logger(__name__, 100)

#-------------------------------------------------------------------------------


class Error(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class Stop(Exception):
    def __init__(self, *args):
        super().__init__(*args)



def jacis_plugin(argv):
    try:
        parser = argparse.ArgumentParser(prog='install')
        parser.add_argument("package", help="package name to install (eg: boost==1.5)")
        parser.add_argument('-v', '--verbose',
            action='count', default=0, help='verbose level')
        # parser.add_argument('-c', '--clean',
        #     action='store_true', default=False, help='clean previous one. Kills all previous data')
        args = parser.parse_args(argv)

        # Update logger
        global log
        log = core.get_logger(__name__, args.verbose)

        log.debug("Hi I'm: {} {}".format(__name__, argv))
        log.debug("Parsed args: {}".format(args))

        install(args.package)

    except Stop as e:
        log.warning(e)
    except Error as e:
        log.error(e)
        sys.exit(1)
    except Exception as e:
        log.critical(e)
        raise


#-------------------------------------------------------------------------------
from jacis.plugins import sync

def in_cache(*relative):
    return os.path.join(core.jacis_global_dir(), "cache", *relative)


def update_repo():
    # repo = sync.auto_repo('git', "https://github.com/ddolzhenko/package_info.git",
    #     local=in_cache('repo'))
    # repo.pull()
    pass

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

def install(package_id):

    update_repo()

    installed = packages.LocalPackageList(in_cache('installed'))
    if package_id in installed:
        raise Stop('{} already installed'.format(package_id))

    available = packages.RepoPackageList(in_cache('repo'))
    if package_id not in available:
        raise Error('unknown package: "{}"'.format(package_id))

    installed.install(available[package_id])


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#--------

class Test(utils.TestCase):

    def test_1(self):

        jacis_plugin(['gtest==1.7.0', '-v'])