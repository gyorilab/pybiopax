__all__ = ['BioPaxObject', 'Entity', 'Pathway', 'Gene']
import re

namespaces = {
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'xsd': 'http://www.w3.org/2001/XMLSchema#',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'bp': 'http://www.biopax.org/release/biopax-level3.owl#'
}


def nselem(ns, elem):
    return '{%s}%s' % (namespaces[ns], elem)


def nssuffix(ns, suffix):
    return '%s%s' % (namespaces[ns], suffix)


def get_datatype(attrib):
    return attrib.get(nselem('rdf', 'datatype'))


def get_resource(attrib):
    res = attrib.get(nselem('rdf', 'resource'))
    if res and res.startswith('#'):
        return res[1:]


def is_datatype(attrib, datatype):
    return get_datatype(attrib) == datatype


def get_tag(element):
    return re.match(r'.*}(.+)', element.tag).groups()[0]


def get_attr_tag(element):
    raw_tag = get_tag(element)
    return camel_to_snake(raw_tag)


def get_id_or_about(element):
    return element.attrib.get(nselem('rdf', 'ID')) or \
        element.attrib.get(nselem('rdf', 'about'))


def get_ns(element):
    return re.match(r'\{(.*)\}', element.tag).groups()[0]


def has_ns(element, ns):
    return get_ns(element) == namespaces[ns]


def camel_to_snake(txt):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', txt).lower()


class Unresolved():
    def __init__(self, obj_id):
        self.obj_id = obj_id


class BioPaxObject:
    list_types = ['xref']

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
            if is_datatype(child.attrib, nssuffix('xsd', 'string')):
                val_to_add = child.text
            else:
                res = get_resource(child.attrib)
                val_to_add = Unresolved(res)
            if key in cls.list_types:
                kwargs[key].append(val_to_add)
            else:
                kwargs[key] = val_to_add
        return cls(**kwargs)


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
