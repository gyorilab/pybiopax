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
            cls = globals()[get_tag(element)]
            obj = cls.from_xml(element)
            objects[obj] = obj

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
                if isinstance(val, Unresolved):
                    setattr(obj, attr, objects[val.obj_id])

        return cls(objects)


