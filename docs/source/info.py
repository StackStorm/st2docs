# -*- coding: utf-8 -*-
#
# This file contains values that differ between open-source
# to commercial (BWC) documentation. Everything that might
# change from one version to another in conf.py should be
# placed here, otherwise you WILL break the build
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, '../../st2'))
sys.path.append(ROOT_DIR + '/st2common')

from st2common import __version__

master_doc = 'index'

project = u'StackStorm'
copyright = u'2016, StackStorm'
author = u'Brocade Communications Inc'

base_url = u'http://docs.stackstorm.com/'
htmlhelp_basename = 'StackStormDoc'

man_pages = [
    ('index', 'stackstorm', u'StackStorm Documentation',
     [u'StackStorm team'], 1)
]
latex_documents = [
    (master_doc, 'stackstorm-docs.tex', u'StackStorm Documentation',
     u'StackStorm team', 'manual'),
]
texinfo_documents = [
    ('index', 'StackStorm', u'StackStorm Documentation',
     u'StackStorm team', 'StackStorm', 'One line description of project.',
     'Miscellaneous'),
]

github_repo = 'StackStorm/st2docs'
github_version = 'master' if __version__.endswith('dev') else 'v' + __version__

theme_base_url = u'http://docs.stackstorm.com/'
