# -*- coding: utf-8 -*-
__authors__ = 'Kirill S. Yakovenko, '
__email__ = 'contacts@crystalnix.com'
__copyright__ = 'Copyright 2014, Crystalnix'

from factory import containers, declarations


class AttributeBuilder(containers.AttributeBuilder):

    def build(self, create, force_sequence=None, prefix=''):
        """Build a dictionary of attributes.

        Args:
            create (bool): whether to 'build' or 'create' the subfactories.
            force_sequence (int or None): if set to an int, use this value for
                the sequence counter; don't advance the related counter.
        """
        # Setup factory sequence.
        if force_sequence is None:
            sequence = self.factory._generate_next_sequence()
        else:
            sequence = force_sequence

        if prefix:
            prefix += '-'

        # Parse attribute declarations, wrapping SubFactory and
        # OrderedDeclaration.
        wrapped_attrs = {}
        for k, v in self._attrs.items():
            if isinstance(v, declarations.OrderedDeclaration):
                v = containers.OrderedDeclarationWrapper(v,
                                                         sequence=sequence,
                                                         create=create,
                                                         extra=self._subfields.get(k, {}),
                )
            wrapped_attrs[prefix + k] = v

        stub = containers.LazyStub(wrapped_attrs, containers=self._containers,
                                   model_class=self.factory, log_ctx=self._log_ctx)
        return stub.__fill__()