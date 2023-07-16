# -*- coding: utf-8 -*-

"""
keys.py
~~~~~~~

This file contains the private keys for tmdbsimple.

See:
    https://developers.themoviedb.org/3/getting-started/introduction
    https://developers.themoviedb.org/3/getting-started/authentication
    https://developers.themoviedb.org/3/authentication/how-do-i-generate-a-session-id
"""

import os

import requests

API_KEY = os.environ.get('TMDB_API_KEY') or '1ce9398920594a5521f0d53e9b33c52f'
USERNAME = os.environ.get('TMDB_USERNAME') or 'bharm01'
PASSWORD = os.environ.get('TMDB_PASSWORD') or 'dogtej-xapqeB-gyqvo7'
SESSION_ID = os.environ.get('TMDB_SESSION_ID') or 'f33501a3e1de5d559f16e1baa98bcd839cc143c2'
