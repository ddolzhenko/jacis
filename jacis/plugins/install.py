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

import jacis

#-------------------------------------------------------------------------------


class Error(Exception):
    def __init__(self, *args):
        super().__init__(*args)





def jacis_plugin(argv):
    try:
        parser = argparse.ArgumentParser(prog='install')
        parser.add_argument("package", help="package name to install (eg: boost)")
        parser.add_argument("version", help="version name to install (eg. 1.50)")
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

        request = Package(args, package, args.version)
        install(request)

    except NothingToDo as e:
        log.warning(e)
    except Error as e:
        log.error(e)
        sys.exit(1)
    except Exception as e:
        log.critical(e)
        raise

        boost@1.5
        1.5@boost

#-------------------------------------------------------------------------------

def install(package_id):
    installed = load_installed_packages_info()
    if package_id in installed:
        raise Stop('already installed')

    available = load_available_packages_info()
    package = available[apackage_id]

    cache(package)

#-------------------------------------------------------------------------------

from jacis.plugins import sync

def cache_dir(realtive=''):
    return os.path.join(core.get_jacis.dir(), "cache", realtive)


def load_available_packages_info():
    local_path = cache_dir('repo')
    local_list = cache_dir('repo/list.yml')
    sync.auto_repo('git', "https://github.com/ddolzhenko/package_info.git", local=local_path, pull=True)
    with open(local_list) as f:
        return PackageList(yaml.load(f))


def load_installed_packages_info():
    installed_list = cache_dir('installed.yml')
    with open(installed_list) as f:
        return PackageList(yaml.load(f))


class PackageInfo:
    def __init__(self, path=''):
        self._available = load_available_packages_info()
        self._installed = load_installed_packages_info()

    def have_local(package):
        return package in self._local_packages



class PackagesCache:
    def __init__(self):
        remote_packages = load_remote()
        my_packages = load_my()



class Test(utils.TestCase):

    def test_1(self):
        PackagesInfo info(core.jacis_global_dir())