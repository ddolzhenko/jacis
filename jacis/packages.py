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

"""Packages manager
"""

#-------------------------------------------------------------------------------

__author__ = "Dmitry Dolzhenko"
__email__  = "d.dolzhenko@gmail.com"

#-------------------------------------------------------------------------------

import os, uuid, time

from jacis import core, utils

log = core.get_logger(__name__, 100)

#-------------------------------------------------------------------------------

import yaml

def __include(loader, node):
    filename = loader.construct_scalar(node) + '.yml'
    with open(filename, 'r') as f:
        return yaml.load(f)

yaml.add_constructor('!include', __include)

#-------------------------------------------------------------------------------

def get_scope(db, upper_scope_variables, reserved_words):
    if db is None:
        db = {}

    scope_variables = {k:v for k,v in db.items() if k not in reserved_words }
    local_variables = upper_scope_variables.copy()
    local_variables.update(scope_variables)
    return local_variables

def walk_packages(names, db, upper_scope_variables, reserved_words):
    if db is None:
        db = {}

    package_scope = get_scope(db, upper_scope_variables, reserved_words)
    mask = '{}.{}'
    for key, pdb in db.get('packages', {}).items():
        yield from walk_packages(names+[key], pdb, package_scope, reserved_words)

    for ver, vdb in db.get('versions', {}).items():
        version_scope = get_scope(vdb, package_scope, reserved_words)
        name = '{}=={}'.format('.'.join(names), ver)
        yield (name, Package(names, ver, vdb, version_scope))


class Package:

    def __format_param(self, param):
        if isinstance(param, list):
            return [self.__format_param(x) for x in  param]
        elif isinstance(param, dict):
            return { k : self.__format_param(v) for k, v in param.items()}
        elif isinstance(param, str):
            return param.format(**self._scope)
        return param

    def __init__(self, names, version, db, upper_scope_variables):
        self._name = names
        self._version = version
        self._pid = '{}=={}'.format('.'.join(names), version)
        self._scope = upper_scope_variables.copy()
        self._scope['self'] = self
        self._db = db

        # format prams with dictionary recursively
        self._scope = self.__format_param(self._scope)

    @property
    def version(self):
        return self._version

    @property
    def pid(self):
        return self._pid



    def __act(self, action, params):
        params = list(map(lambda x: self._scope.get(x), params))
        log.debug('executing {}({})'.format(action, params))

        from jacis.plugins import sync
        actions = {
            'sync': sync.store
        }

        func = actions.get(action)
        if not func:
            raise Exception('unknown command: {}'.format(action))
        func(*params)






    def __execute(self, what):
        script = self._scope['scripts'][what]

        if isinstance(script, str):
            script = [script]

        for action_str in script:
            action = action_str.split(' ')
            self.__act(action[0], action[1:])


    def store(self, path):
        utils.mktree(path)
        with utils.work_dir(path):
            self.__execute('store')

        return dict(name=self.pid, path=path, hash=utils.checksum(path))





class RepoPackageList:
    def __init__(self, path):
        base = 'list.yml'
        self._reserved = set(['packages', 'versions'])
        self._fullpath = os.path.join(path, base)
        with utils.work_dir(path):
            with open(base) as f:
                db = yaml.load(f)
                self._packages = dict(walk_packages([], db, {}, self._reserved))

    def __contains__(self, pid):
        return pid in self._packages

    def __getitem__(self, pid):
        return self._packages[pid]

    def __str__(self):
        return '\n'.join(self._packages.keys())

class LocalPackageList:
    def __init__(self, path):
        self._installed_dir = path
        self._fullpath = os.path.join(path, 'list.yml')
        self.reload()

    def __file_modtime(self):
        return time.ctime(os.path.getmtime(self._fullpath))

    def __file_modified(self):
        self._db_time < self.__file_modtime()


    def reload(self):
        with open(self._fullpath) as f:
            db = yaml.load(f)
            self._db = db if db else {}
            self._db_time = self.__file_modtime()

    def dump(self):
        with open(self._fullpath, 'w') as f:
            yaml.dump(self._db, f, indent=4)
        self._db_time = self.__file_modtime()

    def __contains__(self, pid):
        return pid in self._db

    def __getitem__(self, pid):
        return self._db[pid]

    def __str__(self):
        return '\n'.join(self._db.keys())

    def install(self, package):
        log.debug('installing package: ' + package.pid)
        with utils.work_dir(self._installed_dir):
            # store_dir = str(uuid.uuid5(uuid.NAMESPACE_DNS, package.pid))
            store_dir = package.pid
            info = package.store(store_dir)
            log.debug('package {} stored in {}, result = {}'.format(package.pid, store_dir, info))

            self._db[package.pid] = info
            self.dump();





class TestPackage(utils.TestCase):

    def test_1(self):
        plist = RepoPackageList('d:\\src\\repos\\package_info\\')
        print(plist)

