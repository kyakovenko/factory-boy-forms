# -*- coding: utf-8 -*-
__author__ = 'Kirill S. Yakovenko'
__email__ = 'kirill.yakovenko@gmail.com'
__copyright__ = 'Copyright 2014, Kirill S. Yakovenko'

import six
from factory.base import BaseFactory, FactoryMetaClass, FactoryOptions, OptionDefault

from .converters import converters
from .containers import AttributeBuilder

ATTRIBUTES_STRATEGY = 'attributes'


def fields_for_form(form_class, fields=None, exclude=None, settings=None):
    converter = None
    factory_fields = {}
    settings = settings or {}

    for c in converters:
        if c.can_convert(form_class):
            converter = c
    if converter is None:
        raise ValueError("There is no appropriate converter for '{0}' form".format(form_class.__class__.__name__))

    for name, field in six.iteritems(form_class.base_fields):
        if fields and name not in fields:
            continue
        elif exclude and name in exclude:
            continue
        factory_fields[name] = converter.convert(form_class, field, settings.get(name, {}))
    return factory_fields


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


class FormFactoryOptions(FactoryOptions):

    def _build_default_options(self):
        return [
            OptionDefault('form', None, inherit=True),
            OptionDefault('prefix', '', inherit=True),
            OptionDefault('fields', None, inherit=True),
            OptionDefault('exclude', (), inherit=True),
            OptionDefault('settings', {}, inherit=True),
            OptionDefault('converter', None, inherit=True),
            OptionDefault('abstract', False, inherit=False),
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


# class BaseFormSetFactory(BaseFormFactory):
#
#     @classmethod
#     def attributes(cls, create=False, extra=None, prefix=None, count=None):
#         data = super(BaseFormSetFactory, cls).attributes(create, extra, prefix)
#         if count is None:
#             count = cls._count or 1
#         if prefix is None:
#             prefix = cls._form_prefix
#         for i in xrange(count):
#             subprefix = '{0}-{1}'.format(prefix, i)
#             data.update(
#                 cls._sub_factory.attributes(create, extra, subprefix)
#             )
#         return data


class FormFactory(six.with_metaclass(FormFactoryMetaClass, BaseFormFactory)):
    pass


# class FormSetFactory(six.with_metaclass(FormFactoryMetaClass, BaseFormSetFactory)):
#     pass
