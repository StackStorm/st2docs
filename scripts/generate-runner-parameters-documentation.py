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
import re
from collections import OrderedDict

from pytablewriter import RstGridTableWriter as Writer

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

RUNNER_GROUP_COMMAND = 'Command'
RUNNER_GROUP_DESTINATION = 'Destination'
RUNNER_GROUP_CREDENTIALS = 'Credentials'
RUNNER_GROUP_ACCESS = 'Access'
RUNNER_GROUP_CONNECTION = 'Connection'
RUNNER_GROUP_COMMON_FLAGS = 'Common Flags'
RUNNER_GROUP_DEBUG = 'Debug'

RUNNER_PARAMETER_MAPPINGS = OrderedDict([
    (RUNNER_GROUP_COMMAND, (
        'cmd',
    )),
    (RUNNER_GROUP_DESTINATION, (
        'dir',
    )),
    (RUNNER_GROUP_CREDENTIALS, (
        'username',
        'password',
        'hosts',
        'host',
        'port',
        'private_key',
        'passphrase',
    )),
    (RUNNER_GROUP_ACCESS, (
        'sudo',
        'sudo_password',
    )),
    (RUNNER_GROUP_CONNECTION, (
        'bastion_host',
        'parallel',
        'scheme',
        'transport',
        'verify_ssl_cert',
    )),
    (RUNNER_GROUP_COMMON_FLAGS, (
        'cwd',
        'env',
        'kwarg_op',
        'timeout',
    )),
    (RUNNER_GROUP_DEBUG, (
        'content_version',
        'debug',
    )),
])


def generate_runner_parameter_quick_reference_table(all_runner_names):
    runner_names = []
    runners = {}
    for runner_name in sorted(all_runner_names):
        if runner_name != 'python-script' and (runner_name.endswith('cmd') or runner_name.endswith('script')):
            runner_names.append(runner_name)
            runner_driver = get_backend_driver(runner_name)
            runner_metadata = runner_driver.get_metadata()
            runner_parameters = runner_metadata.get('runner_parameters', [])
            runners[runner_name] = []
            for parameter in runner_parameters:
                runners[runner_name].append(parameter)

    table_header = runner_names.copy()
    table_header.insert(0, 'Runner')
    parameters = []
    for runner_group, runner_parameters in RUNNER_PARAMETER_MAPPINGS.items():
        if runner_parameters:
            parameters.append([f'{runner_group}'])
        for i, parameter in enumerate(runner_parameters):
            if i > 0:
                parameters.append([''])
            for runner_name in runner_names:
                if parameter in runners[runner_name]:
                    parameters[-1].append(f'``{parameter}``')
                    runners[runner_name].remove(parameter)
                else:
                    parameters[-1].append('')

    # Add any unrecognized parameters in an 'Other' group
    if any(runners.values()):
        other_parameters = set()
        for runner_parameters in runners.values():
            other_parameters |= set(runner_parameters)
        if other_parameters:
            parameters.append(['Other'])
        for i, parameter in enumerate(sorted(other_parameters)):
            if i > 0:
                parameters.append([''])
            for runner_name in runner_names:
                if parameter in runners[runner_name]:
                    parameters[-1].append(f'``{parameter}``')
                    runners[runner_name].remove(parameter)
                else:
                    parameters[-1].append('')

    writer = Writer(
        margin=1,
        headers=table_header,
        value_matrix=parameters)

    return post_process_quick_reference_table(writer.dumps())


def post_process_quick_reference_table(table_string):
    output = table_string.split('\n')

    # Figure out the replacement text
    # Example:
    #
    # .. table::
    #
    #     +--------------+-----------------+--------------------+------------------+---------------------+-----------------+-----------------+-----------------+
    #     |   Runners    | local-shell-cmd | local-shell-script | remote-shell-cmd | remote-shell-script |    winrm-cmd    |  winrm-ps-cmd   | winrm-ps-script |
    #     +==============+=================+====================+==================+=====================+=================+=================+=================+
    #     | Runners      | local-shell-cmd | local-shell-script | remote-shell-cmd | remote-shell-script | winrm-cmd       | winrm-ps-cmd    | winrm-ps-script |
    #     +--------------+-----------------+--------------------+------------------+---------------------+-----------------+-----------------+-----------------+
    #     | Command      | cmd             |                    | cmd              |                     | cmd             | cmd             |                 |
    #     +--------------+-----------------+--------------------+------------------+---------------------+-----------------+-----------------+-----------------+
    #     | Destination  |                 |                    | dir              | dir                 |                 |                 |                 |
    #     +--------------+-----------------+--------------------+------------------+---------------------+-----------------+-----------------+-----------------+
    #     | Credentials  |                 |                    | username         | username            | username        | username        | username        |
    #
    #     +-----------
    # ^^^^
    # left_margin
    #
    #     |
    #     +-----------
    #     ^
    #     border
    #
    #     +-----------
    #      ^^^^^^^^^^^
    #      column_width
    #
    separator_row_rgx = re.compile(r'^(?P<margin>\s+)(?P<separator_row>\+(?P<dashes>-+))(?=\+)')
    separator_row_m = separator_row_rgx.match(output[2])

    left_margin = separator_row_m.group('margin')
    left_margin_width = len(left_margin)

    column_width = len(separator_row_m.group('dashes'))

    separator_row = separator_row_m.group('separator_row')
    column_width_with_border = len(separator_row)

    group_title_rgx = re.compile(r'^\s+\|\s+(?:\w+\s+)+\|')

    for i in range(5, len(output)-1):
        m = separator_row_rgx.match(output[i])
        if m:
            group_title_m = group_title_rgx.match(output[i+1])
            if not group_title_m and output[i+1]:
                output[i] = separator_row_rgx.sub(f"{left_margin}|{' '*column_width}", output[i], count=1)

    return '\n'.join(output)


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

    # Generate and write out the quick reference table
    quick_ref_file = '../docs/source/_includes/runner_parameters/quick_reference.rst'
    quick_ref_destination = os.path.join(CURRENT_DIR, quick_ref_file)
    quick_ref_table = generate_runner_parameter_quick_reference_table(runner_names)

    with open(quick_ref_destination, 'w+') as f:
        f.write(quick_ref_table)


if __name__ == '__main__':
    main()
