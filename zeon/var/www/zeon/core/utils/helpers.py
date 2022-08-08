# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present by ChuDoTvoreC
"""
# from collections import defaultdict


class DotDict(dict):
    """Dot.notation access to dictionary attributes"""

    def __getattr__(self, *args):  # __getattr__ = dict.get
        if isinstance(super().__getitem__(*args), dict):
            return DotDict(super().__getitem__(*args))
        if isinstance(super().__getitem__(*args), list):
            return [DotDict(el) for el in super().__getitem__(*args)]
        return super().__getitem__(*args)

    __setattr__ = dict.__setattr__
    __delattr__ = dict.__delattr__


class Templates(object):

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass

    def do(self, method, params=None):
        return "ok"

    def __getattr__(self, attr):
        """Dynamically create an object class (ie: host)"""
        return TemplatesObjectClass(attr, self)


class TemplatesObjectClass(object):
    def __init__(self, name, parent):
        self.parent = parent
        self.name = name

    def __getattr__(self, attr):
        """Dynamically create a method (ie: get)"""

        def fn(*args, **kwargs):
            if args and kwargs:
                raise TypeError("Found both args and kwargs")

            return self.parent.do(
                '{0}.{1}.{2}'.format(self.parent.result, self.name, attr),
                args or kwargs
            )

        # return fn
        if attr == "get":
            return fn
        else:
            self.parent.result = '{0}.{1}'.format(self.name, attr)
            return self.parent
