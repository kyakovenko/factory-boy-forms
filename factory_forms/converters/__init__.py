# -*- coding: utf-8 -*-
__authors__ = 'Kirill S. Yakovenko, '
__email__ = 'contacts@crystalnix.com'
__copyright__ = 'Copyright 2014, Crystalnix'

import unicodedata as ud

all_unicode = ''.join(unichr(i) for i in xrange(65536))
unicode_letters = ''.join(c for c in all_unicode if ud.category(c) == 'Lu' or ud.category(c) == 'Ll')


class FakeConverter(object):

    @staticmethod
    def can_convert(form):
        return False


#try:
from .django import DjangoFormConverter
#except ImportError:
#    DjangoFormConverter = FakeConverter
#    DjangoFormSetConverter = FakeConverter

converters = [DjangoFormConverter, ]


def fields_for_form(form_class, fields=None, exclude=None, settings=None):
    factory_fields = {}
    converter_class = None
    settings = settings or {}

    for c in converters:
        if c.can_convert(form_class):
            converter_class = c
    if converter_class is None:
        raise ValueError("There is no appropriate converter for '{0}' form".format(form_class.__class__.__name__))
    converter = converter_class(form_class)

    for name, field in converter.fields():
        if fields and name not in fields:
            continue
        elif exclude and name in exclude:
            continue
        factory_fields[name] = converter.convert_field(form_class, field, settings.get(name, {}))
    return factory_fields