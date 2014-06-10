# -*- coding: utf-8 -*-
__author__ = 'Kirill S. Yakovenko'
__email__ = 'kirill.yakovenko@gmail.com'
__copyright__ = 'Copyright 2014, Crystalnix'

from datetime import datetime
from nose.tools import assert_raises, assert_equal

from .. import fuzzy


def test_date_time_template():
    now = datetime.now()
    date_time_format = '%d/%m/%y %H:%M:%S %Z'
    date_time_template = fuzzy.DateTimeTemplate(now, date_time_format)

    assert_raises(TypeError, iter, date_time_template)
    assert_equal(repr(date_time_template), now.strftime(date_time_format))
    assert_equal(unicode(date_time_template), now.strftime(date_time_format))
