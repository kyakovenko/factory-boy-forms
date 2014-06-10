# -*- coding: utf-8 -*-
__author__ = 'Kirill S. Yakovenko'
__email__ = 'kirill.yakovenko@gmail.com'
__copyright__ = 'Copyright 2014, Kirill S. Yakovenko'
__all__ = [
    'construct_factory_from_form',
]

from .factories import FormFactory#, FormSetFactory


def construct_factory_from_form(form_class, fields=None, exclude=None, settings=None):

    meta_class = type('Meta', (), {
        'form': form_class,
        'fields': fields,
        'exclude': exclude,
        'settings': settings or {}
    })
    return type('{0}Factory'.format(form_class.__class__.__name__), (FormFactory, ), {'Meta': meta_class})
