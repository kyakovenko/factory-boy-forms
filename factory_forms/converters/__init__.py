# -*- coding: utf-8 -*-
__authors__ = 'Kirill S. Yakovenko, '
__email__ = 'contacts@crystalnix.com'
__copyright__ = 'Copyright 2014, Crystalnix'

import unicodedata as ud

all_unicode = ''.join(unichr(i) for i in xrange(65536))
unicode_letters = ''.join(c for c in all_unicode if ud.category(c) == 'Lu' or ud.category(c) == 'Ll')


class FakeConverter(object):

    def can_convert(self, form):
        return False


try:
    from .django import DjangoFormConverter
except ImportError:
    DjangoFormConverter = FakeConverter

converters = [DjangoFormConverter(), ]