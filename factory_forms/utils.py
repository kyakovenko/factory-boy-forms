# -*- coding: utf-8 -*-
__author__ = 'Kirill S. Yakovenko'
__email__ = 'kirill.yakovenko@gmail.com'
__copyright__ = 'Copyright 2014, Kirill S. Yakovenko'
__all__ = [
    'construct_factory_from_form',
    'construct_post_test',
    'construct_get_test',
]

import six

from django import forms
from factory import Factory
from factory.base import FACTORY_CLASS_DECLARATION

from .factories import FormConverter


def construct_factory_from_form(form_class, fields, exclude, settings):
    factory_fields = {}
    converter = FormConverter()
    for name, field in six.iteritems(form_class.base_fields):
        if fields and name not in fields:
            continue
        elif exclude and name in exclude:
            continue
        factory_fields[name] = converter.convert(form_class, field, settings.get(name, {}))
    form_class_name = type(form_class).__name__
    if issubclass(form_class, forms.ModelForm):
        factory_fields[FACTORY_CLASS_DECLARATION] = form_class._meta.model
    else:
        factory_fields['ABSTRACT_FACTORY'] = False
    return type('{0}Factory'.format(form_class_name), (Factory, ), factory_fields)

