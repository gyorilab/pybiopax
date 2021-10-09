"""This module implements finding paths in a BioPaxModel starting from a
given object using a path constraint string."""
__all__ = ['find_objects', 'BiopaxClassConstraintError']

import logging
import itertools
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

    Returns
    -------
    :
        A list of BioPaxObjects satisfying the given path specification.
    """
    parts = path_str.split('/')
    last = True if len(parts) == 1 else False
    for part in parts:
        if ':' in part:
            attribute, class_constraint_str = part.split(':', maxsplit=1)
            try:
                cls = biopax_cls_map[class_constraint_str]
            except KeyError as e:
                raise BiopaxClassConstraintError(f'{class_constraint_str} '
                                                 f'is not a valid BioPax class '
                                                 f'name.')
        else:
            attribute, cls = part, None

        if attribute.endswith('*'):
            attribute = attribute[:-1]
            recursive = True
        else:
            recursive = False

        # Get the attribute we are looking for
        attr_val = getattr(start_obj, attribute, None)
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

        # If it's a single object
        if isinstance(val, BioPaxObject):
            if cls and not isinstance(val, cls):
                return []
            if not last:
                return find_objects(val, '/'.join(parts[1:]))
            else:
                return [val]
        # If it's a list of objects
        elif isinstance(val, list):
            results = []
            for v in val:
                if not isinstance(v, BioPaxObject):
                    continue
                if cls and not isinstance(v, cls):
                    continue
                if not last:
                    results.append(find_objects(v, '/'.join(parts[1:])))
                else:
                    results.append([v])
            return list(itertools.chain(*results))
        # Otherwise it's a value other than a BioPaxObject which we don't
        # consider here
        else:
            return []


def _get_object_list(val):
    if isinstance(val, BioPaxObject):
        return [val]
    elif isinstance(val, list):
        return [v for v in val if isinstance(v, BioPaxObject)]
    else:
        return []


def _make_biopax_cls_map():
    import inspect
    from pybiopax import biopax
    return {k: v for k, v in inspect.getmembers(biopax, inspect.isclass)
            if issubclass(v, BioPaxObject)}


biopax_cls_map = _make_biopax_cls_map()


class BiopaxClassConstraintError(Exception):
    pass