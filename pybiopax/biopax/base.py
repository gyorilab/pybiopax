__all__ = ['BioPaxObject', 'Entity', 'Pathway', 'Gene', 'Unresolved']

from lxml.etree import Element
from typing import List, ClassVar, Mapping, Optional, Union, TYPE_CHECKING

from ..xml_util import (
    get_datatype, get_attr_tag,get_resource, is_datatype, get_tag,
    get_id_or_about, nssuffix, is_url, makers, nselem, snake_to_camel,
)

if TYPE_CHECKING:
    from .util import PathwayStep, BioSource
    from .interaction import Interaction


class Unresolved:
    def __init__(self, obj_id):
        self.obj_id = obj_id


class BioPaxObject:
    """Generic BioPAX Object. It is the parent class of all more specific
    BioPAX classes."""

    list_types: ClassVar[List[str]] = ['xref', 'comment', 'name']
    xml_types: ClassVar[Mapping[str, str]] = {}

    def __init__(
        self,
        uid: str,
        name: Optional[str] = None,
        comment: Optional[List[str]] = None,
        xref: Optional[List["Xref"]] = None,
    ):
        self.uid = uid
        # TODO: is name in the right place here?
        self.name = name
        self.comment = comment
        # TODO: is xref in the right place here?
        self.xref = xref

    def __repr__(self) -> str:
        s = f"{self.__class__.__name__}(uid={self.uid}"
        if self.name is not None:
            s += f", name={self.name}"
        #if self.comment:
        #    s += f", comment={self.comment}"
        if self.xref:
            s += f", xref={self.xref}"
        s += ")"
        return s

    @classmethod
    def from_xml(cls, element: Element) -> "BioPaxObject":
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

    def to_xml(self) -> Element:
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

    def _simple_to_xml(self, attr: str, val) -> Optional[Element]:
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
    list_types: ClassVar[List[str]] = BioPaxObject.list_types + \
        ['evidence', 'data_source']

    def __init__(self,
                 standard_name: Optional[str] = None,
                 display_name: Optional[str] = None,
                 all_names: Optional[str] = None,
                 participant_of: Optional[str] = None,
                 availability: Optional[str] = None,
                 data_source: Optional[List[str]] = None,
                 evidence: Optional[List[str]] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.standard_name = standard_name
        self.display_name = display_name
        self.all_names = all_names
        self.participant_of = participant_of
        self.availability = availability
        self.data_source = data_source
        self.evidence = evidence

    def __repr__(self) -> str:
        return (
            f"Entity(standard_name={self.standard_name}, display_name={self.display_name}, "
            f"all_names={self.all_names}, participant_of={self.participant_of}, "
            f"availability={self.availability}, data_source={self.data_source},"
            f"evidence={self.evidence})"
        )


class Gene(Entity):
    """BioPAX Gene"""
    def __init__(self, organism: Optional["BioSource"] = None, **kwargs):
        super().__init__(**kwargs)
        self.organism = organism

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(standard_name={self.standard_name}, display_name={self.display_name}, "
            f"all_names={self.all_names}, participant_of={self.participant_of}, "
            f"availability={self.availability}, data_source={self.data_source}, "
            f"evidence={self.evidence}, organism={self.organism})"
        )


class Pathway(Entity):
    """BioPAX Pathway."""
    list_types: ClassVar[List[str]] = Entity.list_types + ['pathway_component']

    def __init__(self,
                 pathway_component: Optional[List[Union["Interaction", "Pathway"]]] = None,
                 pathway_order: Optional[List["PathwayStep"]] = None,
                 organism: Optional["BioSource"] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.pathway_component = pathway_component
        self.pathway_order = pathway_order
        self.organism = organism

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(standard_name={self.standard_name}, display_name={self.display_name}, "
            f"all_names={self.all_names}, participant_of={self.participant_of}, "
            f"availability={self.availability}, data_source={self.data_source}, "
            f"evidence={self.evidence}, pathway_component={self.pathway_component}, "
            f"pathway_order={self.pathway_order}, organism={self.organism})"
        )


# These are necessary to have the objects in the global
# scope, required for some modes of deserialization
from .interaction import *
from .physical_entity import *
from .util import *
