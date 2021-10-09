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

        val = getattr(start_obj, attribute, None)
        if val is None:
            return []
        elif isinstance(val, BioPaxObject):
            if cls and not isinstance(val, cls):
                return []
            if not last:
                return find_objects(val, '/'.join(parts[1:]))
            else:
                return [val]
        elif isinstance(val, list):
            results = []
            for v in val:
                if cls and not isinstance(v, cls):
                    continue
                if not last:
                    results.append(find_objects(v, '/'.join(parts[1:])))
                else:
                    results.append([v])
            return list(itertools.chain(*results))


def _make_biopax_cls_map():
    import inspect
    from pybiopax import biopax
    return {k: v for k, v in inspect.getmembers(biopax, inspect.isclass)
            if issubclass(v, BioPaxObject)}


biopax_cls_map = _make_biopax_cls_map()


class BiopaxClassConstraintError(Exception):
    pass