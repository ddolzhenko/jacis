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

from jacis import core, utils, packages, folder_initializer

#-------------------------------------------------------------------------------

log = core.get_logger(__name__)

#-------------------------------------------------------------------------------

class Error(Exception):
    pass

class Stop(Exception):
    pass

#-------------------------------------------------------------------------------

def jacis_plugin(argv):
    try:
        parser = argparse.ArgumentParser(prog='install')
        parser.add_argument("package", help="package name to install (eg: boost==1.5)")
        parser.add_argument('-v', '--verbose',
            action='count', default=0, help='verbose level')
        parser.add_argument('-f', '--forced',
            action='store_true', default=False, help='clean previous one. Kills all previous data')
        args = parser.parse_args(argv)

        core.set_log_verbosity(args.verbose)

        #hack list
        if args.package=='list':
            list_them()
        else:
            install(args.package, forced=args.forced)

    except Stop as e:
        log.warning(e)
    except Error as e:
        log.error(e)
    except Exception as e:
        log.critical(e)
        raise


#-------s------------------------------------------------------------------------

def in_cache(*relative):
    return os.path.join(core.jacis_global_dir(), "cache", *relative)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

def install(package_id, forced=False):

    folder_initializer.init_global(quiet=True)

    installed = packages.LocalPackageList(in_cache('installed'))
    if package_id in installed:
        if forced:
            installed.remove(package_id)
        else:
            raise Stop('{} already installed'.format(package_id))

    available = packages.RepoPackageList(in_cache('available'))
    if package_id not in available:
        raise Error('unknown package: "{}"'.format(package_id))

    installed.install(available[package_id])


def list_them():

    folder_initializer.init_global(quiet=True)

    installed = packages.LocalPackageList(in_cache('installed'))
    available = packages.RepoPackageList(in_cache('available'))
    log.info('installed:')
    for x in installed.names():
        log.info('    ' + x)

    log.info('----------------------------------------------------')
    log.info('available:')
    for x in available.names():
        log.info('    ' + x)
    log.info('----------------------------------------------------')


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#--------

class Test(utils.TestCase):

    def test_1(self):

        jacis_plugin(['gtest==1.0.0', '-vvv', '-f'])
        jacis_plugin(['gtest==1.5.0', '-vvv', '-f'])
        # jacis_plugin(['boost==1.59.0', '-v'])