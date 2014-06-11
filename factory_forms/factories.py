# -*- coding: utf-8 -*-
__author__ = 'Kirill S. Yakovenko'
__email__ = 'kirill.yakovenko@gmail.com'
__copyright__ = 'Copyright 2014, Kirill S. Yakovenko'

import six
from factory.base import BaseFactory, FactoryMetaClass, FactoryOptions, OptionDefault

from .converters import fields_for_form
from .containers import AttributeBuilder

ATTRIBUTES_STRATEGY = 'attributes'


class FormFactoryMetaClass(FactoryMetaClass):

    def __call__(cls, *args, **kwargs):
        return cls.attributes(*args, **kwargs)

    def __new__(cls, class_name, bases, attrs):
        new_class = super(FormFactoryMetaClass, cls).__new__(cls, class_name, bases, attrs)
        meta = new_class._meta
        declared_fields = meta.declarations
        if meta.form:
            fields = fields_for_form(meta.form, meta.fields, meta.exclude, meta.settings)
            meta.form_fields = fields
            fields.update(declared_fields)
        else:
            fields = declared_fields
        meta.declarations = fields
        return new_class


class FormSetFactoryMetaClass(FactoryMetaClass):

    def __new__(cls, class_name, bases, attrs):
        new_class = super(FormSetFactoryMetaClass, cls).__new__(cls, class_name, bases, attrs)
        meta = new_class._meta
        declared_fields = meta.declarations
        if meta.form:
            fields = fields_for_form(meta.form, meta.fields, meta.exclude, meta.settings, meta.force)
            meta.form_fields = fields
            fields.update(declared_fields)
        else:
            fields = declared_fields
        meta.declarations = fields
        return new_class


class FormFactoryOptions(FactoryOptions):

    def _build_default_options(self):
        return [
            OptionDefault('form', None, inherit=True),
            OptionDefault('prefix', '', inherit=True),
            OptionDefault('fields', None, inherit=True),
            OptionDefault('exclude', None, inherit=True),
            OptionDefault('settings', {}, inherit=True),
            OptionDefault('converter', None, inherit=True),
            OptionDefault('abstract', False, inherit=False),
            OptionDefault('force', False, inherit=True),
            OptionDefault('strategy', ATTRIBUTES_STRATEGY, inherit=True),
        ]

    def _fill_from_meta(self, meta, base_meta):
        super(FormFactoryOptions, self)._fill_from_meta(meta, base_meta)
        self.model = getattr(self.form, 'model', self.form)


class BaseFormFactory(BaseFactory):
    _options_class = FormFactoryOptions
    _meta = FormFactoryOptions()
    _OLDSTYLE_ATTRIBUTES = {}

    @classmethod
    def attributes(cls, create=False, extra=None, prefix=None):
        """Build a dict of attribute values, respecting declaration order.

        The process is:
        - Handle 'orderless' attributes, overriding defaults with provided
            kwargs when applicable
        - Handle ordered attributes, overriding them with provided kwargs when
            applicable; the current list of computed attributes is available
            to the currently processed object.
        """
        if prefix is None:
            prefix = cls._meta.prefix or ''
        force_sequence = None
        if extra:
            force_sequence = extra.pop('__sequence', None)
        log_ctx = '%s.%s' % (cls.__module__, cls.__name__)
        return AttributeBuilder(cls, extra, log_ctx=log_ctx).build(
            create=create,
            force_sequence=force_sequence,
            prefix=prefix
        )


class FormFactory(six.with_metaclass(FormFactoryMetaClass, BaseFormFactory)):
    pass

