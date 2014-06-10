# -*- coding: utf-8 -*-
__authors__ = 'Kirill S. Yakovenko, '
__email__ = 'contacts@crystalnix.com'
__copyright__ = 'Copyright 2014, Crystalnix'

from factory import containers
from nose.tools import assert_true, assert_equal

from ..containers import AttributeBuilder


class FakeFactory(object):
    @classmethod
    def declarations(cls, extra):
        d = {'one': 1}
        d.update(extra)
        return d

    @classmethod
    def _generate_next_sequence(cls):
        return 1


def test_attribute_builder_class():
    assert_true(issubclass(AttributeBuilder, containers.AttributeBuilder))


def test_build_data_with_prefix():
    ab = AttributeBuilder(FakeFactory)
    assert_equal({'one': 1}, ab.build(create=False))

    assert_equal({'test-one': 1}, ab.build(create=False, prefix='test'))