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
available action parameters.
"""

import os

import yaml

# from st2common.content.loader import RunnersLoader, RUNNER_MANIFEST_FILE_NAME

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DOC_HEADER = '.. NOTE: This file has been generated automatically, don\'t manually edit it\n'
H1 = 32
H2 = 70
HORIZONTAL_BORDER = '   ' + '='*H1 + '  ' + '='*H2
FULL_COLUMN_SPAN = '   ' + '-'*H1 + '--' + '-'*H2
HEADINGS = '   ' + '{:34}'.format('Parameter') + 'Description'
REQUIRED_HEADER = '   **Required:**'
OPTIONAL_HEADER = '   **Optional:**'


def _create_list(foldername, fulldir=True, suffix=".yaml"):
    file_list_tmp = os.listdir(foldername)
    file_list = []
    if fulldir:
        for item in file_list_tmp:
            if item.endswith(suffix):
                file_list.append(os.path.join(foldername, item))
    else:
        for item in file_list_tmp:
            if item.endswith(suffix):
                file_list.append(item)
    return file_list


def _get_actions():
    actions = []
    actions_dir = os.path.join(CURRENT_DIR, '../dcfabric/packs/dcfabric/actions')
    action_file_list = _create_list(actions_dir)

    for metadata_path in action_file_list:
        with open(metadata_path, 'r') as metadata_file:
            metadata_contents = metadata_file.read()
            metadata = yaml.safe_load(metadata_contents)

            actions.append(metadata)

    return actions


ACTIONS = _get_actions()


def main():
    for action in ACTIONS:
        result = []
        required_params = []
        optional_params = []
        result.append(DOC_HEADER)
        result.append(action['name'])
        result.append('~'*len(action['name']))
        result.append('')
        description_line = '**Description**: %(description)s ' % action
        result.append(description_line)
        result.append('')
        result.append('.. table::\n')
        result.append(HORIZONTAL_BORDER)
        result.append(HEADINGS)
        result.append(HORIZONTAL_BORDER)
        results_body = [None] * len(action['parameters'])

        for name, values in action['parameters'].items():
            if values.get('description'):
                name = '*' + name + '*'
                # Make parameter name bold for required params
                if values.get('required', False):
                    name = '*' + name + '*'
                values['type'] = '``' + values['type'] + '``'
                values['name'] = name
                details = []
                details.append('   %(name)-32s  %(description)s\n' % values)
                if values.get('enum'):
                    details.append('   ' + ' '*H1 + '  Choose from:\n')
                    for enum_val in values.get('enum'):
                        details.append('   ' + ' '*H1 + '  - ' + str(enum_val))
                else:
                    details.append('   ' + ' '*H1 + '  Type: ' + values['type'])
                if values.get('default'):
                    details.append('\n' +
                                   '   ' + ' '*H1 + '  **Default**: ' + str(values['default']))
                # Figure out what position to insert this parameter in the table
                print values['description']
                position = values['position']
                results_body[position] = '\n'.join(details)

        result.extend(results_body)
        result.append(HORIZONTAL_BORDER)
        result.append('\n')
        file_name = action['name'].replace('-', '_')
        path = '../docs/source/_includes/solutions/dcfabric/%s.rst' % (file_name)
        destination_path = os.path.join(CURRENT_DIR, path)
        result = '\n'.join(result)
        with open(destination_path, 'w') as fp:
            fp.write(result)

if __name__ == '__main__':
    main()
