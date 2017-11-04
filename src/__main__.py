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

from termify import *
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--translation', help='show the translation of the lyrics')

    return parser.parse_args()


def main():
    """Display lyrics"""
    try:
        args = get_args()
        if args.translation:
            get_lyrics_translate(args.translation)
        else:
            get_lyrics()

    except Exception as e:
        print(AsciiTable([[e_lyrics_not_found], ['Cause: ' + str(e)]], 'Error').table)
