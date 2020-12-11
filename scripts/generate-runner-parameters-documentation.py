#!/usr/bin/env python
# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Script which generates documentation section which contains information about
available runner parameters.
"""

import os

from st2common.runners import get_available_backends
from st2common.runners import get_backend_driver

__all__ = [
    'main'
]


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
HEADER = """\
.. NOTE: This file has been generated automatically, do not manually edit it.
         If you want to update runner parameters, make your changes to the
         runner YAML files in st2/contrib/runners/ and then run

         make docs

         to regenerate the documentation for runners.
"""

def main():
    runner_names = get_available_backends()
    for runner_name in runner_names:
        runner_driver = get_backend_driver(runner_name)
        runner_metadata = runner_driver.get_metadata()

        if runner_metadata.get('experimental', False):
            continue

        result = []
        result.append(HEADER)
        result.append('')

        runner_parameters = runner_metadata.get('runner_parameters', None)
        if runner_parameters:
            for name, values in runner_parameters.items():
                format_values = {'name': name}
                format_values.update(values)
                line = '* ``%(name)s`` (%(type)s) - %(description)s' % format_values
                result.append(line)

            file_name = runner_metadata['name'].replace('-', '_')
            path = '../docs/source/_includes/runner_parameters/%s.rst' % (file_name)
            destination_path = os.path.join(CURRENT_DIR, path)
            result = '\n'.join(result)

            with open(destination_path, 'w') as fp:
                fp.write(result)

if __name__ == '__main__':
    main()
