# -*- coding: utf-8 -*-
#
# This file contains values that differ between open-source
# to commercial (EWC) documentation. Everything that might
# change from one version to another in conf.py should be 
# placed here, otherwise you WILL break the build.

from datetime import datetime

master_doc = 'index'

project = "StackStorm"
copyright = "2014 - %s, StackStorm" % (datetime.now().strftime("%Y"))
author = "The StackStorm Authors"

base_url = "https://docs.stackstorm.com/"
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

github_user = "StackStorm"
github_repo = "st2docs"
github_version = "master"
