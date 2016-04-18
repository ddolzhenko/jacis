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

"""Supply  package s index
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
        parser = argparse.ArgumentParser(prog='supply')
        parser.add_argument("package", default="", help="package name to install (eg: boost==1.5.0)")

        parser.add_argument('--remove',
            action='store_true', default=False, help='just remove package')

        parser.add_argument('--available',
            action='store_true', default=False, help='show available packages similarly named')
        parser.add_argument('--installed',
            action='store_true', default=False, help='show installed packages similarly named')

        parser.add_argument('-f', '--forced',
            action='store_true', default=False, help='remove previous one and all previous package data')

        parser.add_argument('-v', '--verbose',
            action='count', default=0, help='verbose level')
        args = parser.parse_args(argv)

        core.set_log_verbosity(args.verbose)

        folder_initializer.init_global(quiet=True)


        if args.available or args.installed:
            if args.available:
                core.set_log_verbosity(max(args.verbose, 1))
                list_available_packages(args.package)
            if args.installed:
                core.set_log_verbosity(max(args.verbose, 1))
                list_installed_packages(args.package)
        else:
            if args.remove:
                remove_package(args.package, args.forced)
            else:
                install_package(args.package, forced=args.forced)


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

def install_package(package_id, forced=False):

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


br = lambda: log.info('----------------------------------------------------')
tab = lambda x: '    ' + x

def list_available_packages(package_id):
    like = lambda pid: package_id in pid
    available = packages.RepoPackageList(in_cache('available'))
    br()
    log.info('available:')
    for x in available.names():
        if like(x):
            log.info(tab(x))
    br()

def list_installed_packages(package_id):
    like = lambda pid: package_id in pid
    installed = packages.LocalPackageList(in_cache('installed'))
    br()
    log.info('installed:')
    for x in installed.names():
        if like(x):
            log.info(tab(x))
    br()

def remove_package(package_id, forced=False):
    installed = packages.LocalPackageList(in_cache('installed'))
    if package_id not in installed:
        raise Error('{} package not installed'.format(package_id))

    installed.remove(package_id)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#--------

class Test(utils.TestCase):

    def test_1(self):
        log.warning('\n>>>>> list available <<<<<<<:')
        jacis_plugin(['gtest==1', '--available', '-vvv'])

        log.warning('\n>>>>> installing <<<<<<<:')
        jacis_plugin(['gtest==1.0.0', '-vvv', '-f'])

        log.warning('\n>>>>> list installed <<<<<<<:')
        jacis_plugin(['gtest', '--installed', '-vvv'])

        log.warning('\n>>>>> remove installed <<<<<<<:')
        jacis_plugin(['gtest==1.0.0', '--remove', '-vvv'])

        log.warning('\n>>>>> remove not installed <<<<<<<:')
        jacis_plugin(['gtest==1.0.0', '--remove', '-vvv'])

        log.warning('\n>>>>> list installed <<<<<<<:')
        jacis_plugin(['gtest', '--installed', '-vvv'])
