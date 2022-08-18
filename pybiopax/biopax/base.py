__all__ = ['BioPaxObject', 'Controller', 'Entity', 'Pathway', 'Gene',
           'Unresolved', 'Observable', 'Named', 'XReferrable']

from typing import List, Optional, TYPE_CHECKING

from ..xml_util import *

if TYPE_CHECKING:
    from .util import Xref


class Unresolved:
    """A placeholder class used while deserializing BioPAX models."""
    def __init__(self, obj_id):
        self.obj_id = obj_id


class BioPaxObject:
    """Generic BioPAX Object. It is the parent class of all more specific
    BioPAX classes."""
    list_types = ['comment']
    xml_types = {}

    def __init__(self, uid, comment=None, **kwargs):
        # Pass on for cooperative inheritance
        super().__init__(**kwargs)
        self.uid = uid
        self.comment = comment if comment else []

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
                    or is_datatype(child.attrib, 'xsd', 'string') \
                    or is_datatype(child.attrib, 'xsd', 'int') \
                    or is_datatype(child.attrib, 'xsd', 'float'):
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

            # We have to implement special handling for names to make sure
            # we don't serialize display/standard names here
            if attr == 'name' and isinstance(self, Named):
                val = self.get_plain_names()

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


class XReferrable:
    """A mixin class to add xrefs to a BioPaxObject.

    Attributes
    ----------
    xref : List[Xref]
    """
    list_types = ['xref']

    def __init__(self, xref: Optional[List["Xref"]] = None, **kwargs):
        # Pass on for cooperative inheritance
        super().__init__(**kwargs)
        self.xref = xref if xref else []


class Named(XReferrable):
    """A mixin class to add names to a BioPaxObject.

    Attributes
    ----------
    display_name : str
    standard_name : str
    name : str
    """
    list_types = XReferrable.list_types + ['name']

    def __init__(self, display_name=None, standard_name=None, name=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.display_name = display_name
        self.standard_name = standard_name
        self._name = name if name else []

    @property
    def name(self):
        """All names associated with the object including the standard and
        display name, if available."""
        std_name = [self.standard_name] if self.standard_name else []
        disp_name = [self.display_name] if self.display_name else []
        return std_name + disp_name + self._name

    def get_plain_names(self):
        return self._name


class Observable:
    """A mixin class to add evidence to a BioPaxObject.

    Attributes
    ----------
    evidence : List[Evidence]
    """
    list_types = ['evidence']

    def __init__(self, evidence=None, **kwargs):
        # Pass on for cooperative inheritance
        super().__init__(**kwargs)
        self.evidence = evidence if evidence else []


class Entity(BioPaxObject, Observable, Named):
    """BioPAX Entity.

    Attributes
    ----------
    availability : str
    data_source : List[Provenance]
    """
    list_types = BioPaxObject.list_types + Observable.list_types + \
        Named.list_types + ['data_source']

    def __init__(self,
                 availability=None,
                 data_source=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.availability = availability
        self.data_source = data_source if data_source else []
        self._participant_of = set()

    @property
    def participant_of(self):
        return self._participant_of


class Gene(Entity):
    """BioPAX Gene

    Attributes
    ----------
    organism: BioSource
    """
    def __init__(self, organism, **kwargs):
        super().__init__(**kwargs)
        self.organism = organism


class Controller:
    """BioPAX Controller."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._controller_of = set()

    @property
    def controller_of(self):
        return self._controller_of


class Pathway(Entity, Controller):
    """BioPAX Pathway."""
    list_types = Entity.list_types + ['pathway_component']

    def __init__(self,
                 pathway_component=None,
                 pathway_order=None,
                 organism=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.pathway_component = pathway_component if pathway_component else []
        self.pathway_order = pathway_order
        self.organism = organism


# These are necessary to have the objects in the global
# scope, required for some modes of deserialization
from .interaction import *
from .physical_entity import *
from .util import *
