__all__ = ['BioPaxObject', 'Entity', 'Pathway', 'Gene', 'Unresolved']

from ..xml_util import *


class Unresolved:
    def __init__(self, obj_id):
        self.obj_id = obj_id


class BioPaxObject:
    """Generic BioPAX Object. It is the parent class of all more specific
    BioPAX classes."""
    list_types = ['xref', 'comment']
    xml_types = {}

    def __init__(self, uid, name=None, comment=None, xref=None):
        self.uid = uid
        # TODO: is name in the right place here?
        self.name = name
        self.comment = comment
        # TODO: is xref in the right place here?
        self.xref = xref

    @classmethod
    def from_xml(cls, element):
        uid = get_id_or_about(element)
        kwargs = {'uid': uid}
        for key in cls.list_types:
            kwargs[key] = []
        for child in element.getchildren():
            key = get_attr_tag(child)
            # In some OWL formats, the child is directly defined
            # under this tag, in that case we directly deserialize it.
            if child.getchildren():
                gchild = child.getchildren()[0]
                obj_cls = globals()[get_tag(gchild)]
                val_to_add = obj_cls.from_xml(gchild)
            # Otherwise, we check if the element is a simple type that we
            # can just get as a text value
            elif (get_datatype(child.attrib) is None
                  and not get_resource(child.attrib)) \
                    or is_datatype(child.attrib, nssuffix('xsd', 'string')) \
                    or is_datatype(child.attrib, nssuffix('xsd', 'int')) \
                    or is_datatype(child.attrib, nssuffix('xsd', 'float')):
                val_to_add = child.text
            # If neither of the above is the case, then we assume that the
            # element is a reference that is defined in another block
            # somewhere so we treat is as Unresolved until later.
            else:
                res = get_resource(child.attrib)
                val_to_add = Unresolved(res)

            if key in cls.list_types:
                kwargs[key].append(val_to_add)
            else:
                kwargs[key] = val_to_add
        return cls(**kwargs)

    def to_xml(self):
        id_type = 'about' if is_url(self.uid) else 'ID'
        element = makers['bp'](self.__class__.__name__,
                               **{nselem('rdf', id_type): self.uid})
        for attr in [a for a in dir(self)
                     if not a.startswith('_')
                     and a not in {'list_types', 'xml_types',
                                   'to_xml', 'from_xml', 'uid'}]:
            val = getattr(self, attr)
            if val is None:
                continue
            if isinstance(val, list):
                for v in val:
                    child_elem = self._simple_to_xml(attr, v)
                    if child_elem is not None:
                        element.append(child_elem)
            else:
                child_elem = self._simple_to_xml(attr, val)
                if child_elem is not None:
                    element.append(child_elem)
        return element

    def _simple_to_xml(self, attr, val):
        if isinstance(val, BioPaxObject):
            child_elem = makers['bp'](
                snake_to_camel(attr),
                **{nselem('rdf', 'resource'):
                    ('#%s' % val.uid) if not is_url(val.uid) else val.uid}
            )
            return child_elem
        elif isinstance(val, str):
            xml_type = self.xml_types.get(attr, 'string')
            child_elem = makers['bp'](
                snake_to_camel(attr),
                val,
                **{nselem('rdf', 'datatype'): nssuffix('xsd', xml_type)}
            )
            return child_elem
        return None


class Entity(BioPaxObject):
    """BioPAX Entity."""
    list_types = BioPaxObject.list_types + \
        ['evidence', 'data_source']

    def __init__(self,
                 standard_name=None,
                 display_name=None,
                 all_names=None,
                 participant_of=None,
                 availability=None,
                 data_source=None,
                 evidence=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.standard_name = standard_name
        self.display_name = display_name
        self.all_names = all_names
        self.participant_of = participant_of
        self.availability = availability
        self.data_source = data_source
        self.evidence = evidence


class Gene(Entity):
    """BioPAX Gene"""
    def __init__(self, organism, **kwargs):
        super().__init__(**kwargs)
        self.organism = organism


class Pathway(Entity):
    """BioPAX Pathway."""
    list_types = Entity.list_types + ['pathway_component']

    def __init__(self,
                 pathway_component=None,
                 pathway_order=None,
                 organism=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.pathway_component = pathway_component
        self.pathway_order = pathway_order
        self.organism = organism


# These are necessary to have the objects in the global
# scope, required for some modes of deserialization
from .interaction import *
from .physical_entity import *
from .util import *
