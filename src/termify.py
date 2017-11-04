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

"""Termify is a simple service that permits you to retrieve lyrics in your terminal."""

from terminaltables import AsciiTable
from osascript import osascript
from bs4 import BeautifulSoup
import re
import requests


# Service Settings
service_provider = 'https://www.musixmatch.com/'
service_language = {
    'en': ['lyrics/', '/translation/english'],
    'es': ['lyrics/', '/translation/spanish'],
    'it': ['it/testo/', '/traduzione/italiano'],
    'fr': ['fr/paroles/', '/traduction/francais'],
    'jp': ['ja/lyrics/', '/translation/japanese'],
    'de': ['de/songtext/', '/ubersetzung/deutsche'],
    'ko': ['ko/lyrics/', '/translation/korean'],
    'pt': ['pt/letras/', '/traducao/portugues'],
    'pt-br': ['pt-br/letras/', '/traducao/portugues']
}

# User Settings
user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko)'}

# Error Messages
e_lyrics_not_found = 'Sorry! An error occurred while trying to retrieve the lyrics'


def get_artist_name():
    """Retrieve the artist name playing in the Spotify"""
    return osascript(
        """tell app "Spotify"
                return artist of current track
            end tell
        """
    )[1]


def get_track_name():
    """Retrieve the song title playing in the Spotify"""
    return osascript(
        """tell app "Spotify"
                return name of current track
            end tell
        """
    )[1]


def get_track_info():
    """Retrieve the track information playing in the Spotify"""
    return get_artist_name() + '/' + get_track_name()


def uglify(word):
    """Remove spaces and unused chars"""
    return re.sub('\s+', '-', word.replace('-', ''))


def get_lyrics():
    """Get and print the lyrics of a track from service provider"""
    try:
        url = service_provider + service_language['en'][0] + uglify(get_track_info())
        html_content = requests.get(url, headers=user_agent).content
        html_parsing = BeautifulSoup(html_content, 'html.parser')
        lyrics = [['Original']]

        for music_snippet in html_parsing.find_all('p', {'class': 'mxm-lyrics__content'}):
            lyrics.append([music_snippet.get_text().encode('utf-8')])

        print(AsciiTable(lyrics, get_track_info()).table)
        print(url)

    except Exception as e:
        print(AsciiTable([[e_lyrics_not_found], ['Cause: ' + str(e)]], 'Error').table)


def get_lyrics_translate(lang):
    """Get and print the lyrics translate of a track from service provider"""
    try:
        url = service_provider + service_language[lang][0] + uglify(get_track_info()) + service_language[lang][1]
        html_content = requests.get(url, headers=user_agent).content
        html_parsing = BeautifulSoup(html_content, 'html.parser')
        lyrics_translate = [['Original', 'Translation']]

        for music_snippet in html_parsing.find_all('div', {'class': 'mxm-translatable-line-readonly'}):
            original = music_snippet.find('div', {'class': 'col-xs-6'}).get_text().encode('utf-8')
            translation = music_snippet.find('div', {'class': 'col-xs-6'}).next_sibling.get_text().encode('utf-8')
            lyrics_translate.append([original, translation])

        print(AsciiTable(lyrics_translate, get_track_info()).table)
        print(url)

    except Exception as e:
        print(AsciiTable([[e_lyrics_not_found], ['Cause: ' + str(e)]], 'Error').table)
