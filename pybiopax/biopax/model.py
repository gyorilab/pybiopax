__all__ = ['BioPaxModel']

from . import *
from ..xml_util import has_ns, get_id_or_about, get_tag, wrap_xml_elements


class BioPaxModel:
    """BioPAX Model.

    Parameters
    ----------
    objects : dict
        A dict of BioPaxObject instances keyed by their URI string.

    Attributes
    ----------
    objects : dict
        A dict of BioPaxObject instances keyed by their URI string
        that are part of the model.
    """
    def __init__(self, objects):
        self.objects = objects

    @classmethod
    def from_xml(cls, tree):
        """Return a BioPAX Model from an OWL/XML element tree."""
        objects = {}
        for element in tree.getchildren():
            if not has_ns(element, 'bp'):
                continue
            id = get_id_or_about(element)
            obj_cls = globals()[get_tag(element)]
            obj = obj_cls.from_xml(element)
            objects[id] = obj

        for obj_id, obj in objects.items():
            for attr in [a for a in dir(obj) if not a.startswith('__')]:
                val = getattr(obj, attr)
                resolved_val = resolve_value(objects, val)
                setattr(obj, attr, resolved_val)

        return cls(objects)

    def to_xml(self):
        """Return an OWL string from the content of the model."""
        elements = [obj.to_xml() for obj in self.objects.values()]
        return wrap_xml_elements(elements)


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
