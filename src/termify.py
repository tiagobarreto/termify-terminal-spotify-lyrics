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


# Service Provider
service_provider = 'https://www.musixmatch.com/'

# Service Language
service_language = {
    'en': ['lyrics/', '/translation/english'],
    'it': ['it/testo/', '/translation/italian'],
    'fr': ['fr/paroles/', '/translation/french'],
    'jp': ['ja/lyrics/', '/translation/japanese'],
    'de': ['de/songtext/', '/translation/german'],
    'ko': ['ko/lyrics/', '/translation/korean'],
    'pt': ['pt/letras/', '/translation/portuguese'],
    'pt-br': ['pt-br/letras/', '/translation/portuguese']
}

# User Agent
user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko)'}


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
    return get_artist_name() + "/" + get_track_name()


def uglify(word):
    """Remove spaces and unused chars"""
    return re.sub('\s+', '-', word.replace("-", ""))


def get_lyrics(lang, has_translation):
    """Print the lyrics of a track from service provider"""
    try:
        url = service_provider + service_language[lang][0] + uglify(get_track_info())
        if has_translation:
            url.append(service_language[lang][1])
        html_content = requests.get(url, headers=user_agent).content
        html_parsing = BeautifulSoup(html_content, 'html.parser')
        lyrics = [[url], []]

        for music_snippet in html_parsing.find_all('p', {'class': "mxm-lyrics__content"}):
            lyrics.append([str(music_snippet.get_text())])

        print(AsciiTable(lyrics, get_track_info()).table)

    except Exception as e:
        print(AsciiTable(
            [
                ['Sorry! An error occurred while trying to retrieve the lyrics'],
                ['Cause: ' + str(e)]
            ], 'Error').table)