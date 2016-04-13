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

import jacis.utils
import jacis.core

from jacis.utils import work_dir

log = jacis.core.get_logger(__name__, 100)

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
    def __init__(self, names, version, db, upper_scope_variables):
        self._name = names
        self.version = version
        self._scope = upper_scope_variables.copy()
        self._db = db


class PackageList:
    def __init__(self, path):
        self._reserved = set(['packages', 'versions'])
        with work_dir(path):
            with open('list.yml') as f:
                db = yaml.load(f)
                self._packages = dict(walk_packages([], db, {}, self._reserved))

    def __str__(self):
        return '\n'.join(self._packages.keys())


class TestPackage(jacis.utils.TestCase):

    def test_1(self):
        plist = PackageList('d:\\src\\repos\\package_info\\')
        print(plist)

