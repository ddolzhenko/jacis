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

"""Config class
"""

#-------------------------------------------------------------------------------

__author__ = "Dmitry Dolzhenko"
__email__  = "d.dolzhenko@gmail.com"

#-------------------------------------------------------------------------------

import inspect
import yaml

from jacis import core

log = core.get_logger(__name__)

#-------------------------------------------------------------------------------
# global properties

package_repo_url = 'https://github.com/ddolzhenko/package_info.git'

#-------------------------------------------------------------------------------

default_filename = '.jacis/config.yml'
default_str = '''
    user:
        name:
        mail:
    '''

class Config:
    def __init__(self, db=yaml.load(default_str)):
        assert isinstance(db, dict)
        for name, value in db.items():
            if isinstance(value, dict):
                setattr(self, name, Config(value))
            else:
                setattr(self, name, value)

    def update(self, db):
        for name, value in db.items():
            attr = getattr(self, name)
            if not attr:
                log.error('attribute "{}" unknown'.format(name))
            else:
                attr = Config(value) if isinstance(value, dict) else value

    def data(self):
        def is_data(x):
            return type(x[1]) in (bool, int, float, list, dict)

        def extract(attr):
            return attr.data() if isinstance(attr, Config) else attr

        attrs = ((name, getattr(self, name)) for name in dir(self))
        attrs = filter(is_data, attrs)
        db = { name : extract(value) for name, value in attrs}

        return db

    def load_file(self, filename=default_filename):
        with open(filename, 'r') as f:
            self.update(yaml.load(f))

    def dump_file(self, filename=default_filename):
        with open(filename, 'w') as f:
            yaml.dump(self.data(), f, width=80, indent=4)


__default_config = None
def get_global():
    '''Load global config'''
    if not __default_config:
        __default_config = Config()

        with utils.work_dir(core.jacis_global_dir()):
            __default_config.load_file()

    return __default_config.copy()

def load():
    '''Load config from current folder (use global as default)'''
    config = get_global()
    config.load_file()
    return config

