import os
import pathlib
import re
from typing import Union

from lxml import etree
from lxml.builder import ElementMaker


namespaces = {
    'xsd': 'http://www.w3.org/2001/XMLSchema#',
    'owl': 'http://www.w3.org/2002/07/owl#',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'bp': 'http://www.biopax.org/release/biopax-level3.owl#',
    'xml': 'http://www.w3.org/XML/1998/namespace'
}


makers = {
    ns: ElementMaker(namespace=prefix)
    for ns, prefix in namespaces.items()
}


def wrap_xml_elements(elements, xml_base):
    """Return a valid BioPAX OWL wrapping XML-serialized BioPAX objects."""
    # We first make the RDF wrapper and add an Ontology element first
    rdfm = ElementMaker(namespace=namespaces['rdf'],
                        nsmap=namespaces)
    rdf_element = rdfm('RDF',
                       **{nselem('xml', 'base'): xml_base})
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
    """Return the OWL string for an XML element tree."""
    xmlb = etree.tostring(xml, pretty_print=True,
                          encoding='utf-8', xml_declaration=True)
    xmls = xmlb.decode('utf-8')
    xmls = '\n'.join([re.sub(r'^  <bp', '\n<bp', x) for x in xmls.split('\n')])
    xmls = '\n'.join([re.sub(r'^  </bp', '</bp', x) for x in xmls.split('\n')])
    xmls = '\n'.join([re.sub(r'^    <', ' <', x) for x in xmls.split('\n')])
    return xmls


def xml_to_file(xml, fname: Union[str, pathlib.Path, os.PathLike]):
    """Write an XML element tree to a given file."""
    with open(fname, 'w') as fh:
        fh.write(xml_to_str(xml))


def nselem(ns, elem):
    """Return a full namespaced string with curly brackets with a suffix."""
    return '{%s}%s' % (namespaces[ns], elem)


def nssuffix(ns, suffix):
    """Return a full namespaced string with a suffix."""
    return '%s%s' % (namespaces[ns], suffix)


def get_datatype(attrib):
    """Return the RDF data type of an element attribute."""
    return attrib.get(nselem('rdf', 'datatype'))


def get_resource(attrib):
    """Return the resource associated with an element attribute."""
    res = attrib.get(nselem('rdf', 'resource'))
    if res:
        if res.startswith('#'):
            return res[1:]
        else:
            return res


def is_url(txt):
    """Return true if the given string is an URL."""
    return txt.startswith('http')


def is_datatype(attrib, prefix, datatype):
    """Return True of the given attribute is of a given type."""
    possibilities = {nssuffix(prefix, datatype),
                     f'{prefix}:{datatype}'}

    return get_datatype(attrib) in possibilities


def get_tag(element):
    """Return the tag of an element."""
    return re.match(r'.*}(.+)', element.tag).groups()[0]


def get_attr_tag(element):
    """Return the tag of an element as an attribute name."""
    raw_tag = get_tag(element)
    return camel_to_snake(raw_tag)


def get_id_or_about(element):
    """Return the ID or the about associated with an element"""
    return element.attrib.get(nselem('rdf', 'ID')) or \
        element.attrib.get(nselem('rdf', 'about'))


def get_ns(element):
    """Return the name space of a given element."""
    return re.match(r'\{(.*)\}', element.tag).groups()[0]


def has_ns(element, ns):
    """Return True if the element is from a given name space."""
    return get_ns(element) == namespaces[ns]


def camel_to_snake(txt):
    """Return snake case from camel case"""
    return re.sub(r'(?<!^)(?=[A-Z])', '_', txt).lower()


def snake_to_camel(txt):
    """Return camel case from snake case."""
    parts = txt.split('_')
    return parts[0] + ''.join([p.capitalize() for p in parts[1:]])
