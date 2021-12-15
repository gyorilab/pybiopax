"""This module implements finding paths in a BioPaxModel starting from a
given object using a path constraint string."""
__all__ = ['find_objects', 'BiopaxClassConstraintError']

import logging
from typing import List
from .biopax import *


logger = logging.getLogger(__name__)


def find_objects(start_obj: BioPaxObject, path_str: str) -> List[BioPaxObject]:
    """Return objects matching the given path specification.

    Parameters
    ----------
    start_obj :
        The object to start the search from.

    path_str :
        A path specification string which consists of one or more parts
        separated by /. Each part is the name of an object attribute, and
        can optionally contain a class name as well, separated by : to
        constrain the class of the target of the attribute to consider.
        Optionally, each attribute can also have a * suffix to make the
        search recursive.

    Returns
    -------
    :
        A list of BioPaxObjects satisfying the given path specification.
    """
    # We split off the first part and separate out the rest
    part, rest = path_str.split('/', maxsplit=1) \
        if '/' in path_str else (path_str, None)

    # Handle class constraint
    if ':' in part:
        attribute, class_constraint_str = part.split(':', maxsplit=1)
        try:
            cls = biopax_cls_map[class_constraint_str]
        except KeyError:
            raise BiopaxClassConstraintError(class_constraint_str) from None
    else:
        attribute, cls = part, None

    # Handle recursion marker
    if attribute.endswith('*'):
        attribute = attribute[:-1]
        recursive = True
    else:
        recursive = False

    # Get the attribute we are looking for
    attr_val = getattr(start_obj, attribute, None)
    # We turn the value into a flat list of BioPaxObjects
    val = _get_object_list(attr_val)

    # If this is a recursive part, we run a BFS to get all the downstream
    # objects that can be reached via one or more of the given type of
    # attribute links
    if recursive:
        queue = val[:]
        visited = val[:]
        while queue:
            obj = queue.pop(0)
            obj_val = getattr(obj, attribute, None)
            for child in _get_object_list(obj_val):
                if child not in visited:
                    visited.append(child)
                    queue.append(child)
        val = visited

    # At this point, val is guaranteed to be a list of BioPaxObjects
    results = []
    for v in val:
        if cls and not isinstance(v, cls):
            continue
        if rest:
            results += find_objects(v, rest)
        else:
            results.append(v)
    return results


def _get_object_list(val):
    if isinstance(val, BioPaxObject):
        return [val]
    elif isinstance(val, (list, set)):
        return [v for v in val if isinstance(v, BioPaxObject)]
    else:
        return []


def _make_biopax_cls_map():
    import inspect
    from pybiopax import biopax
    return {k: v for k, v in inspect.getmembers(biopax, inspect.isclass)
            if issubclass(v, BioPaxObject)}


biopax_cls_map = _make_biopax_cls_map()


class BiopaxClassConstraintError(KeyError):
    def __init__(self, cls_str):
        self.cls_str = cls_str

    def __str__(self):
        return f'{self.cls_str} is not a valid BioPAX class name.'
