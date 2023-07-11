# -*- coding: utf-8 -*-

"""
__init__.py
~~~~~~~~~~~

This test suite checks the methods of tmdbsimple.

Use the following command to run all the tests:
    python -W ignore:ResourceWarning -m unittest discover tests

:copyright: (c) 2013-2022 by Celia Oakley.
:license: GPLv3, see LICENSE for more details.
"""

"""
Either place your API_KEY in the following constant:
"""
# API_KEY = '89b32847c0525854de030aea3a8c5d9d'
API_KEY = 'k_0vtefojw'

"""
or include it in a keys.py file.
"""
try:
    from .keys import API_KEY, USERNAME, PASSWORD, SESSION_ID
except ImportError:
    pass

__all__ = ['API_KEY', 'USERNAME', 'PASSWORD', 'SESSION_ID']
