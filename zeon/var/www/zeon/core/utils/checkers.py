# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present by ChuDoTvoreC

This methods collected from module enum. Not used yet.
"""


def _is_descriptor(obj):
    """
    Returns True if obj is a descriptor, False otherwise.
    """
    return (
            hasattr(obj, '__get__') or
            hasattr(obj, '__set__') or
            hasattr(obj, '__delete__')
            )


def _is_dunder(name):
    """
    Returns True if a __dunder__ name, False otherwise.
    """
    return (
            len(name) > 4 and
            name[:2] == name[-2:] == '__' and
            name[2] != '_' and
            name[-3] != '_'
            )


def _is_sunder(name):
    """
    Returns True if a _sunder_ name, False otherwise.
    """
    return (
            len(name) > 2 and
            name[0] == name[-1] == '_' and
            name[1:2] != '_' and
            name[-2:-1] != '_'
            )


def _is_private(cls_name, name):
    # do not use `re` as `re` imports `enum`
    pattern = '_%s__' % (cls_name, )
    if (
            len(name) >= 5
            and name.startswith(pattern)
            and name[len(pattern)] != '_'
            and (name[-1] != '_' or name[-2] != '_')
        ):
        return True
    else:
        return False


def _make_class_unpicklable(cls):
    """
    Make the given class un-picklable.
    """
    def _break_on_call_reduce(self, proto):
        raise TypeError('%r cannot be pickled' % self)
    cls.__reduce_ex__ = _break_on_call_reduce
    cls.__module__ = '<unknown>'


_auto_null = object()
class auto:
    """
    Instances are replaced with an appropriate value in Enum class suites.
    """
    value = _auto_null


class _EnumDict(dict):
    """
    Track enum member order and ensure member names are not reused.

    EnumMeta will use the names found in self._member_names as the
    enumeration member names.
    """
    def __init__(self):
        super().__init__()
        self._member_names = []
        self._last_values = []
        self._ignore = []
        self._auto_called = False

    def __setitem__(self, key, value):
        """
        Changes anything not dundered or not a descriptor.

        If an enum member name is used twice, an error is raised; duplicate
        values are not checked for.

        Single underscore (sunder) names are reserved.
        """
        if _is_private(self._cls_name, key):
            import warnings
            warnings.warn(
                    "private variables, such as %r, will be normal attributes in 3.10"
                        % (key, ),
                    DeprecationWarning,
                    stacklevel=2,
                    )
        if _is_sunder(key):
            if key not in (
                    '_order_', '_create_pseudo_member_',
                    '_generate_next_value_', '_missing_', '_ignore_',
                    ):
                raise ValueError('_names_ are reserved for future Enum use')
            if key == '_generate_next_value_':
                # check if members already defined as auto()
                if self._auto_called:
                    raise TypeError("_generate_next_value_ must be defined before members")
                setattr(self, '_generate_next_value', value)
            elif key == '_ignore_':
                if isinstance(value, str):
                    value = value.replace(',',' ').split()
                else:
                    value = list(value)
                self._ignore = value
                already = set(value) & set(self._member_names)
                if already:
                    raise ValueError(
                            '_ignore_ cannot specify already set names: %r'
                            % (already, )
                            )
        elif _is_dunder(key):
            if key == '__order__':
                key = '_order_'
        elif key in self._member_names:
            # descriptor overwriting an enum?
            raise TypeError('Attempted to reuse key: %r' % key)
        elif key in self._ignore:
            pass
        elif not _is_descriptor(value):
            if key in self:
                # enum overwriting a descriptor?
                raise TypeError('%r already defined as: %r' % (key, self[key]))
            if isinstance(value, auto):
                if value.value == _auto_null:
                    value.value = self._generate_next_value(
                            key,
                            1,
                            len(self._member_names),
                            self._last_values[:],
                            )
                    self._auto_called = True
                value = value.value
            self._member_names.append(key)
            self._last_values.append(value)
        super().__setitem__(key, value)


# Dummy value for Enum as EnumMeta explicitly checks for it, but of course
# until EnumMeta finishes running the first time the Enum class doesn't exist.
# This is also why there are checks in EnumMeta like `if Enum is not None`
Enum = None
