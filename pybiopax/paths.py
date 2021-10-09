__all__ = ['find_objects', 'BiopaxClassConstraintError']

import logging
import itertools
from .biopax import *


logger = logging.getLogger(__name__)


def find_objects(start_obj: BioPaxObject, path_str: str):
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


class BiopaxClassConstraintError(KeyError):
    pass