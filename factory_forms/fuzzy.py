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


class FuzzyMultiChoice(fuzzy.FuzzyChoice):

    def fuzz(self):
        return [random.choice(self.choices) for _ in xrange(random.randint(1, len(self.choices)))]


class FuzzyRegex(fuzzy.BaseFuzzyAttribute):

    def __init__(self, regex, max_length=None):
        self.regex = regex
        self.max_length = max_length

    def fuzz(self):
        regex = rstr.xeger(self.regex)
        if self.max_length:
            regex = regex[:self.max_length]
        return regex


class FuzzyModelChoiceBase(fuzzy.BaseFuzzyAttribute):

    def __init__(self, queryset, empty_value=None):
        self.queryset = queryset
        self.empty_value = empty_value

    def fuzz(self):
        choices = self.queryset.values_list('pk', flat=True)
        if self.empty_value is not None:
            choices.append(self.empty_value)
        return self.make_choice(choices)

    def make_choice(self, choices):
        raise NotImplementedError


class FuzzyModelChoice(FuzzyModelChoiceBase):

    def make_choice(self, choices):
        return random.choice(choices)


class FuzzyModelMultiChoice(FuzzyModelChoiceBase):

    def make_choice(self, choices):
        start = 1 if self.empty_value is None else 0
        return [random.choice(choices) for _ in xrange(random.randint(start, len(choices)))]
