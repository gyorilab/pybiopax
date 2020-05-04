import re
from .base import *
from .interaction import *
from .physical_entity import *
from .util import *


class Model:
    def __init__(self, objects):
        self.objects = objects

    @classmethod
    def from_xml(cls, tree):
        objects = {}
        for element in tree.getchildren():
            if not has_ns(element, 'bp'):
                continue
            id = get_id_or_about(element)
            obj_cls = globals()[get_tag(element)]
            obj = obj_cls.from_xml(element)
            objects[id] = obj

        """
        objects = {
            element.attrib[nselem('rdf', 'ID')]:
                globals()[get_tag(element)].from_xml(element)
            for element in tree.getchildren()
            if has_ns(element, 'bp')
        }
        """

        for obj_id, obj in objects.items():
            for attr in [a for a in dir(obj) if not a.startswith('__')]:
                val = getattr(obj, attr)
                resolved_val = resolve_value(objects, val)
                setattr(obj, attr, resolved_val)

        return cls(objects)


def resolve_value(objects, val):
    if isinstance(val, Unresolved):
        if val.obj_id not in objects:
            resolved_val = val.obj_id
        else:
            resolved_val = objects[val.obj_id]
    elif isinstance(val, list):
        resolved_val = [resolve_value(objects, v) for v in val]
    else:
        resolved_val = val
    return resolved_val
