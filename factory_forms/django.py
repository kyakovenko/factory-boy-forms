# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

__authors__ = 'Kirill S. Yakovenko, '
__email__ = 'contacts@crystalnix.com'
__copyright__ = 'Copyright 2014, Crystalnix'

import six
from django.forms.formsets import BaseFormSet
from django.forms.formsets import TOTAL_FORM_COUNT, INITIAL_FORM_COUNT, MAX_NUM_FORM_COUNT
from factory.base import OptionDefault

from .utils import construct_factory_from_form
from .factories import BaseFormFactory, FormFactoryMetaClass, FormFactoryOptions


class FormSetFactoryOptions(FormFactoryOptions):

    def _build_default_options(self):
        options = super(FormSetFactoryOptions, self)._build_default_options()
        options.extend((
            OptionDefault('sub_form_factory', None, inherit=False),
            OptionDefault('count', 0, inherit=False),
        ))
        return options


class FormSetFactoryMetaClass(FormFactoryMetaClass):

    def __new__(cls, class_name, bases, attrs):
        new_class = super(FormSetFactoryMetaClass, cls).__new__(cls, class_name, bases, attrs)
        meta = new_class._meta
        declared_fields = meta.declarations
        if meta.form:
            fields = {
                TOTAL_FORM_COUNT: min(meta.form.max_num, meta.form.extra),
                INITIAL_FORM_COUNT: 0,
                MAX_NUM_FORM_COUNT: meta.form.max_num
            }
            meta.count = meta.form.extra
            meta.sub_form_factory = construct_factory_from_form(meta.form.form, meta.fields, meta.exclude, meta.settings)
            fields.update(declared_fields)
        else:
            fields = declared_fields
        meta.prefix = meta.prefix or BaseFormSet.get_default_prefix()
        meta.declarations = fields
        return new_class


class BaseFormSetFactory(BaseFormFactory):

    @classmethod
    def attributes(cls, create=False, extra=None, prefix=None, count=None):
        data = super(BaseFormSetFactory, cls).attributes(create, extra, prefix)
        if count is None:
            count = cls._meta.count
        if prefix is None:
            prefix = cls._meta.prefix
        for i in xrange(count):
            subprefix = '{0}-{1}'.format(prefix, i)
            data.update(
                cls._meta.sub_form_factory.attributes(create, extra, subprefix)
            )
        return data


class FormSetFactory(six.with_metaclass(FormSetFactoryMetaClass, BaseFormSetFactory)):
    pass