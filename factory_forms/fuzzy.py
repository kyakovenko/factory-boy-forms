# -*- coding: utf-8 -*-
__author__ = 'Kirill S. Yakovenko'
__email__ = 'kirill.yakovenko@gmail.com'
__copyright__ = 'Copyright 2014, Kirill S. Yakovenko'

import rstr
import random
from factory import fuzzy
from django.conf import settings
from collections import namedtuple


class DateTimeTemplate(namedtuple('DateTimeTemplate', ('value', 'format'))):

    def __iter__(self):
        raise TypeError

    def __repr__(self):
        return unicode(self)

    def __unicode__(self):
        return self.value.strftime(self.format)


class FuzzyStringDateTime(fuzzy.FuzzyDateTime):

    def __init__(self, *args, **kwargs):
        self.datetime_format = kwargs.pop('format', settings.DATETIME_INPUT_FORMATS[0])
        super(FuzzyStringDateTime, self).__init__(*args, **kwargs)

    def fuzz(self):
        value = super(FuzzyStringDateTime, self).fuzz()
        return DateTimeTemplate(value, self.datetime_format)


class FuzzyFloat(fuzzy.BaseFuzzyAttribute):

    def __init__(self, low, high=None, **kwargs):
        if high is None:
            high = low
            low = 0.0

        self.low = low
        self.high = high
        super(FuzzyFloat, self).__init__(**kwargs)

    def fuzz(self):
        return random.uniform(self.low, self.high)


class FuzzyModelChoice(fuzzy.BaseFuzzyAttribute):

    def __init__(self, choices):
        self.choices = choices

    def fuzz(self):
        choices = list(i[0] for i in self.choices)
        return random.choice(choices)


class FuzzyMultiModelChoice(FuzzyModelChoice):

    def fuzz(self):
        choices = list(i[0] for i in self.choices)
        return [random.choice(choices) for _ in xrange(random.randint(1, len(choices)))]


class FuzzyRegex(fuzzy.BaseFuzzyAttribute):

    def __init__(self, regex, max_length=None):
        self.regex = regex
        self.max_length = max_length

    def fuzz(self):
        regex = rstr.xeger(self.regex)
        if self.max_length:
            regex = regex[:self.max_length]
        return regex