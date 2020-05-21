import re
from lxml import etree
from lxml.builder import ElementMaker


namespaces = {
    'xsd': 'http://www.w3.org/2001/XMLSchema#',
    'owl': 'http://www.w3.org/2002/07/owl#',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'bp': 'http://www.biopax.org/release/biopax-level3.owl#',
    'xml': 'http://www.w3.org/XML/1998/namespace'
}


emaker = ElementMaker(nsmap=namespaces)
bpelem = ElementMaker(namespace=namespaces['bp'],
                                   nsmap={'bp': namespaces['bp']})

makers = {
    ns: ElementMaker(namespace=prefix)
    for ns, prefix in namespaces.items()
}


def wrap_xml_elements(elements):
    # We first make the RDF wrapper and add an Ontology element first
    rdfm = ElementMaker(namespace=namespaces['rdf'],
                        nsmap=namespaces)
    rdf_element = rdfm('RDF',
                       **{nselem('xml', 'base'): 'http://purl.org/pc2/7/'})
    owl_element = makers['owl']('Ontology',
                                **{nselem('rdf', 'about'): ''})
    imports = makers['owl']('imports',
                            **{nselem('rdf', 'resource'): namespaces['bp']})
    owl_element.append(imports)
    rdf_element.append(owl_element)

    for element in elements:
        rdf_element.append(element)
    return rdf_element


def xml_to_str(xml):
    xmlb = etree.tostring(xml, pretty_print=True,
                          encoding='utf-8', xml_declaration=True)
    return xmlb.decode('utf-8')


def xml_to_file(xml, fname):
    with open(fname, 'w') as fh:
        fh.write(xml_to_str(xml))


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
