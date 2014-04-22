# -*- coding: utf-8 -*-
__author__ = 'Kirill S. Yakovenko'
__email__ = 'kirill.yakovenko@gmail.com'
__copyright__ = 'Copyright 2013, Kirill S. Yakovenko'

import unicodedata as ud

all_unicode = ''.join(unichr(i) for i in xrange(65536))
unicode_letters = ''.join(c for c in all_unicode if ud.category(c) == 'Lu' or ud.category(c) == 'Ll')