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

"""Command line interface tests
"""

#-------------------------------------------------------------------------------

__author__ = "Dmitry Dolzhenko"
__email__  = "d.dolzhenko@gmail.com"

#-------------------------------------------------------------------------------

import os
from jacis import utils

#-------------------------------------------------------------------------------

class InternalCommands(utils.TestCase):
    
    def setUp(self):
        utils.temp_work_dir()

    def tearDown(self):
        pass

    def cute(self, msg):
        return "{}. CWD: '{}'".format(msg, self.work_dir)

    def test_full_repo(self):
        
        # import jacis
        import jacis.plugins
        
        print ("\n".join(map(str, jacis.plugins.get_plugins(jacis))))
        # print ("\n".join(map(str, map(type, inspect.getmembers(jacis)[1]))))
        # print(inspect.ismodule(jacis))

        # parser = argparse.ArgumentParser(prog=version.program_name, description=version.program_full_name)
        # x = parser.add_subparsers('init', help="initialize jacis")
        # x.add_parser()
        # init = parser.add_subparsers('init', help="initialize jacis")
        # args = parser.parse_args()



                