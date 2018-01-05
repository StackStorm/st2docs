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

import yaml

from st2common.content.loader import RunnersLoader, RUNNER_MANIFEST_FILE_NAME


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
HEADER = '.. NOTE: This file has been generated automatically, don\'t manually edit it'


def _get_runners_dir():
    runner_loader = RunnersLoader()
    runner_dir = os.path.join(CURRENT_DIR, '../st2/contrib/runners')

    runner_types = runner_loader.get_runners([runner_dir])

    return runner_types


def _get_runners():
    runners = []
    runners_dir = _get_runners_dir()

    for runner, runner_dir in runners_dir.iteritems():
        manifest_path = os.path.join(runner_dir, RUNNER_MANIFEST_FILE_NAME)

        with open(manifest_path, 'r') as manifest_file:
            manifest_contents = manifest_file.read()
            manifest = yaml.load(manifest_contents)

            runners.extend(manifest)

    return runners


RUNNER_TYPES = _get_runners()

def main():
    for runner in RUNNER_TYPES:
        if runner.get('experimental', False):
            continue

        result = []
        result.append(HEADER)
        result.append('')

        for name, values in runner['runner_parameters'].items():
            format_values = {'name': name}
            format_values.update(values)
            line = '* ``%(name)s`` (%(type)s) - %(description)s' % format_values
            result.append(line)

        file_name = runner['name'].replace('-', '_')
        path = '../docs/source/_includes/runner_parameters/%s.rst' % (file_name)
        destination_path = os.path.join(CURRENT_DIR, path)
        result = '\n'.join(result)

        with open(destination_path, 'w') as fp:
            fp.write(result)

if __name__ == '__main__':
    main()
