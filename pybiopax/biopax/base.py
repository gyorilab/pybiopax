__all__ = ['BioPaxObject', 'Entity', 'Pathway', 'Gene', 'Unresolved']

from ..xml_util import *


class Unresolved:
    def __init__(self, obj_id):
        self.obj_id = obj_id


class BioPaxObject:
    list_types = ['xref']
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
            if is_datatype(child.attrib, nssuffix('xsd', 'string')) \
                    or is_datatype(child.attrib, nssuffix('xsd', 'int')) \
                    or is_datatype(child.attrib, nssuffix('xsd', 'float')):
                val_to_add = child.text
            else:
                res = get_resource(child.attrib)
                val_to_add = Unresolved(res)
            if key in cls.list_types:
                kwargs[key].append(val_to_add)
            else:
                kwargs[key] = val_to_add
        return cls(**kwargs)

    def to_xml(self):
        id_type = 'about' if self.uid.startswith('http://') else 'ID'
        element = makers['bp'](self.__class__.__name__,
                               **{nselem('rdf', id_type): self.uid})
        for attr in [a for a in dir(self) if not a.startswith('__')]:
            if attr == 'uid':
                continue
            val = getattr(self, attr)
            if isinstance(val, BioPaxObject):
                child_elem = makers['bp'](
                    snake_to_camel(attr),
                    **{nselem('rdf', 'resource'): ('#%s' % val.uid)}
                )
                element.append(child_elem)
            elif isinstance(val, str):
                xml_type = self.xml_types.get(attr, 'string')
                child_elem = makers['bp'](
                    snake_to_camel(attr),
                    val,
                    **{nselem('rdf', 'resource'): nssuffix('xsd', xml_type)}
                )
                element.append(child_elem)

        return element


class Entity(BioPaxObject):
    list_types = ['evidence']

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
    def __init__(self, organism, **kwargs):
        super().__init__(**kwargs)
        self.organism = organism


class Pathway(Entity):
    pass



"""
Counter({#'participant_stoichiometry': 609,
         #'component_stoichiometry': 1176,
         #'component': 1226,
         #'entity_feature': 4952,
         #'xref': 45216,
         #'left': 358,
         'member_entity_reference': 136,
         #'right': 136,
         #'feature': 1553,
         #'member_physical_entity': 739,
         'evidence': 1262})
"""
