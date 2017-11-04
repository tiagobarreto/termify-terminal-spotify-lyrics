#!/usr/bin/env python

# -*- coding: utf-8 -*-

# termify is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as  by
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# termify is distributed in the hope that it will be useful,
# but without any warranty; without even the implied warranty of
# merchantability or fitness for a particular purpose.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with termify. If not, see < http://www.gnu.org/licenses/ >.
#
# (C) 2017 - by Tiago Barreto, <iam@tiagobarreto.com>

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


requirements = ['requests', 'bs4', 'osascript', 'terminaltables']

setup(
    name="termify",
    version="1.0.0",
    author="Tiago Barreto",
    author_email="iam@tiagobarreto.com",
    description="Termify is a simple service that permits you to retrieve lyrics in your terminal",
    long_description=read('README.md'),
    license="MIT",
    keywords="termify lyrics spotify terminal",
    url="https://github.com/tiagobarreto/termify",
    packages=['src'],
    include_package_data=True,
    install_requires=requirements,
    entry_points={'console_scripts': ['termify=src.__main__:main']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Music :: Lyrics',
         'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4'
)
