#!/usr/bin/env python
#
# -*- mode: python; sh-basic-offset: 4; indent-tabs-mode: nil; coding: utf-8 -*-
# vim: tabstop=4 softtabstop=4 expandtab shiftwidth=4 fileencoding=utf-8

import setuptools

from src import nagii

setuptools.setup(
    name = 'nagii',
    version = nagii.VERSION,
    author = 'Jorge Gallegos',
    author_email = 'kad@blegh.net',
    description = 'A straightforward Nagios modelling library',
    install_requires = [
        'mako',
        'markdown2',
    ],
    packages = setuptools.find_packages('src'),
    package_dir = { '': 'src' },
    zip_safe = True,
    keywords = 'nagios',
    url = 'https://github.com/thekad/nagii',
    license = 'MIT',
)
