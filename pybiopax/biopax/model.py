__all__ = ['BioPaxModel']

import tqdm
from . import *
from ..xml_util import has_ns, get_id_or_about, get_tag, wrap_xml_elements


class BioPaxModel:
    """BioPAX Model.

    Parameters
    ----------
    objects : dict
        A dict of BioPaxObject instances keyed by their URI string.
    xml_base : str
        The XML base namespace for the content being represented.

    Attributes
    ----------
    objects : dict
        A dict of BioPaxObject instances keyed by their URI string
        that are part of the model.
    xml_base : str
        The XML base namespace for the content being represented.
    """
    def __init__(self, objects, xml_base):
        self.objects = objects
        self.xml_base = xml_base

    @classmethod
    def from_xml(cls, tree):
        """Return a BioPAX Model from an OWL/XML element tree."""
        objects = {}
        for element in tqdm.tqdm(tree.getchildren(),
                                 desc='Processing OWL elements'):
            if not has_ns(element, 'bp'):
                continue
            id = get_id_or_about(element)
            obj_cls = globals()[get_tag(element)]
            obj = obj_cls.from_xml(element)
            objects[id] = obj
            # We now register objects that were recursively
            # extracted but have not been registered yet
            sub_objs = get_sub_objects(obj)
            for sub_obj in sub_objs:
                if sub_obj.uid not in objects:
                    objects[sub_obj.uid] = sub_obj

        for obj_id, obj in objects.items():
            for attr in [a for a in dir(obj) if not a.startswith('__')]:
                val = getattr(obj, attr)
                resolved_val = resolve_value(objects, val)
                setattr(obj, attr, resolved_val)

        return cls(objects, tree.base)

    def to_xml(self):
        """Return an OWL string from the content of the model."""
        elements = [obj.to_xml() for obj in self.objects.values()]
        return wrap_xml_elements(elements, self.xml_base)

    def get_objects_by_type(self, obj_type):
        for obj in self.objects.values():
            if isinstance(obj, obj_type):
                yield obj


def get_sub_objects(obj):
    """Get all the children of an object that were extracted and
    are BioPaxObjects that need to be registered in the model."""
    sub_objs = []
    for attr in [a for a in dir(obj) if not a.startswith('__')]:
        val = getattr(obj, attr)
        if isinstance(val, BioPaxObject):
            sub_objs.append(val)
            sub_objs += get_sub_objects(val)
        elif isinstance(val, list):
            for elem in val:
                if isinstance(elem, BioPaxObject):
                    sub_objs.append(elem)
                    sub_objs += get_sub_objects(elem)
    return sub_objs


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
