__all__ = ['BioPaxModel', 'PYBIOPAX_TQDM_CONFIG']

from typing import Any, Mapping, Optional

from tqdm.auto import tqdm

from . import *
from ..xml_util import get_id_or_about, get_tag, has_ns, wrap_xml_elements

default_xml_base = 'http://www.biopax.org/release/biopax-level3.owl#'

PYBIOPAX_TQDM_CONFIG = {"unit_scale": True}
"""Default configuration for tqdm progress bars in pybiopax. To modify
the tqdm configuration, modify this module-level variable. For example,
to disable the progress bars, set the ``disable`` key to ``True``."""


class BioPaxModel:
    """BioPAX Model.

    Parameters
    ----------
    objects : dict or list
        A dict of BioPaxObject instances keyed by their URI string or a list
        of BioPaxObject instances, which will get converted into a dict keyed
        their URI strings
    xml_base : str
        The XML base namespace for the content being represented.

    Attributes
    ----------
    objects : dict
        A dict of BioPaxObject instances keyed by their URI string
        that are part of the model.
    xml_base : Optional[str]
        The XML base namespace for the content being represented. If not
        provided, the default BioPAX Level 3 base namespace is used.
    """

    def __init__(self, objects, xml_base=default_xml_base):
        if isinstance(objects, list):
            self.objects = {o.uid: o for o in objects}
        else:
            self.objects = objects
        self.xml_base = xml_base
        self.add_reverse_links()

    @classmethod
    def from_xml(cls, tree) -> "BioPaxModel":
        """Return a BioPAX Model from an OWL/XML element tree.

        Parameters
        ----------
        tree :
            An element tree from which the model is extracted

        Returns
        -------
        :
            A BioPAX Model deserialized from the OWL XML tree.
        """
        objects = {}
        tqdm_kwargs = {'desc': 'Processing OWL elements'}
        tqdm_kwargs.update(PYBIOPAX_TQDM_CONFIG)
        for element in tqdm(tree, **tqdm_kwargs):
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
            for attr in [a for a in dir(obj) if not a.startswith('_')]:
                # This is to avoid properties
                if attr not in obj.__dict__:
                    continue
                val = getattr(obj, attr)
                resolved_val = resolve_value(objects, val)
                setattr(obj, attr, resolved_val)

        return cls(objects, tree.base)

    def to_xml(self) -> str:
        """Return an OWL string from the content of the model."""
        tqdm_kwargs = {'desc': 'Serializing OWL elements'}
        tqdm_kwargs.update(PYBIOPAX_TQDM_CONFIG)
        elements = [obj.to_xml() for obj in tqdm(self.objects.values(),
                                                 **tqdm_kwargs)]
        return wrap_xml_elements(elements, self.xml_base)

    def get_objects_by_type(self, obj_type):
        for obj in self.objects.values():
            if isinstance(obj, obj_type):
                yield obj

    def add_reverse_links(self):
        for uid, obj in self.objects.items():
            for attr in [a for a in dir(obj) if not a.startswith('_')
                         and a not in {'list_types', 'xml_types',
                                       'to_xml', 'from_xml', 'uid'}]:
                val = getattr(obj, attr)
                if isinstance(val, BioPaxObject) or \
                        (isinstance(val, list) and
                         all(isinstance(v, BioPaxObject) for v in val)):
                    if attr in ['left', 'right']:
                        of_attr = '_participant_of'
                    else:
                        of_attr = '_%s_of' % attr
                    vals = val if isinstance(val, list) else [val]
                    for v in vals:
                        if of_attr in dir(v):
                            of_attr_val = getattr(v, of_attr)
                            of_attr_val.add(obj)


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
