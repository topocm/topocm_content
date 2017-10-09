#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'TU Delft and course contributors'
SITENAME = 'Topology in Condensed Matter'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Amsterdam'

DEFAULT_LANG = 'en'

FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('This course on edX', 'http://tiny.cc/topocm'),
         ('Course chat', 'https://chat.topocondmat.org'),
         ('Source code', 'https://github.com/topocm/topocm_content'),)

ANNOUNCEMENTS = (
    ('<a href="https://quantumtinkerer.tudelft.nl/open_positions/">'
     'We have a PhD position open</a>'),
)




DEFAULT_PAGINATION = 10

MARKUP = ('md', 'ipynb')

PLUGIN_PATHS = ['./plugins']
PLUGINS = ['ipynb.markup']
THEME = "themes/pelican-bootstrap3"

ARCHIVES_SAVE_AS = ''
CATEGORIES_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
TAGS_SAVE_AS = ''
INDEX_SAVE_AS = ''
AUTHOR_SAVE_AS = ''
CATEGORY_SAVE_AS = ''

DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = False
BOOTSTRAP_FLUID = True
SHOW_DATE_MODIFIED = False
SHOW_ARTICLE_INFO = False
SHOW_TITLE_HEADER = False

PIWIK_URL = 'piwik.kwant-project.org'
# PIWIK_SSL_URL
PIWIK_SITE_ID = 4
