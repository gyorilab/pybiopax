import re
import lxml.builder


namespaces = {
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'xsd': 'http://www.w3.org/2001/XMLSchema#',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'bp': 'http://www.biopax.org/release/biopax-level3.owl#'
}

emaker = lxml.builder.ElementMaker(nsmap=namespaces)


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
