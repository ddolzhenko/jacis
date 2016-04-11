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

import uuid
import jacis

#-------------------------------------------------------------------------------


class Error(Exception):
    def __init__(self, *args):
        super().__init__(*args)



def jacis_plugin(argv):
    try:
        parser = argparse.ArgumentParser(prog='install')
        parser.add_argument("package", help="package name to install (eg: boost@1.5)")
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


#-------------------------------------------------------------------------------
from jacis.plugins import sync

def in_cache(realtive=''):
    return os.path.join(core.get_jacis.dir(), "cache", realtive)


def update_repo():
    repo = sync.auto_repo('git', "https://github.com/ddolzhenko/package_info.git",
        local=in_cache('repo'))
    repo.pull()

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

def install(package_id):

    update_repo()

    installed = load_installed_packages_info(in_cache('installed/list.yml'))
    if package_id in installed:
        raise Stop('already installed')

    available = load_available_packages_info(in_cache('repo/list.yml'))
    if package_id not in available:
        raise Error('unknown package: "{}"'.format(package_id))

    installed.process(available[package_id])


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
def normalize_id(package_id):
    return package_id


class Package:

    def __init__(self, pid, data):
        self.pid = normalize_id(pid)
        self.path = data['path']
        self.hash = data['hash']

    def process(self, path):
        self.path = path
        repo_type   = self._sync['type']
        repo_url    = self._sync['url']
        repo = sync.auto_repo(repo_type, repo_url, local=path)
        repo.pull()

        # build

        self.hash = utils.checksum(self.path)
        assert self.is_valid()

    def is_valid(self):
        return utils.checksum(self.path) == self.hash



class PackageList:
    def __init__(self, filename):
        self.filename = filename
        self._reload

    def _reload(self):
        with open(self. filename) as f:
            self.db = yaml.load(f)

    def _flush(self):
        with open(self.filename, 'w') as f:
            yaml.dump(self.db, f)

    #operator in
    def __contains__(self, package_id):
        pid = normalize_id(package_id)
        return pid in self.db

    # operator[]
    def __getitem__(self, package_id):
        pid = normalize_id(package_id)
        return Package(pid, self.db[pid])

    # operator[] = value
    @utils.static_typed(PackageList, str, Package)
    def __setitem__(self, package_id, value):
        pid = Package.normalize_id(package_id)
        self.db[pid] = value

    def process(self, package):
        assert package.pid not in self

        with utils.work_dir(in_cache('installed')):
            store_dir = str(uuid.uuid5(uuid.NAMESPACE_DNS, pid))
            package.process(store_dir)

        self[package.pid] = package
        self._flush();



class Test(utils.TestCase):

    def test_1(self):
        info(core.jacis_global_dir())