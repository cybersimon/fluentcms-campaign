# -*- coding: utf-8 -*-

import collections

from .compat import import_by_path as import_string


def import_callback(func):
    if func is not None:
        if not isinstance(func, collections.Callable):
            func = import_string(func)
        return func
    return None
