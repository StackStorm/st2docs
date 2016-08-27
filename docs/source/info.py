# -*- coding: utf-8 -*-
#
# This file contains values that differ between open-source
# to commercial (BWC) documentation. Everything that might
# change from one version to another in conf.py should be 
# placed here, otherwise you WILL break the build.

master_doc = 'index'

project = u'ipfabric-docs'
copyright = u'2016, Brocade Communications Inc'
author = u'Brocade Communications Inc'

base_url = u'http://bwc-docs.brocade.com/'
htmlhelp_basename = 'ipfabric-doc'

man_pages = [
    ('index', 'ipfabric-docs', u'IPFabric Documentation',
     [u'Brocade'], 1)
]
latex_documents = [
    (master_doc, 'ipfabric-docs.tex', u'ipfabric-docs Documentation',
     u'Brocade Communications Inc', 'manual'),
]
texinfo_documents = [
    (master_doc, 'ipfabric-docs', u'IPFabric Documentation',
     u'Brocade', 'ipfabric-docs', 'One line description of project.',
     'Miscellaneous'),
]

github_repo = 'StackStorm/ipfabric-docs'
github_version = 'master'

theme_base_url = u'http://bwc-docs.brocade.com/'
