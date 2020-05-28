__all__ = ['model_from_owl_str', 'model_from_owl_file', 'model_to_owl_str',
           'model_to_owl_file', 'model_from_owl_url']

import requests
from xml.etree import ElementTree as ET
from .biopax.model import BioPaxModel
from .xml_util import xml_to_str, xml_to_file


def model_from_owl_str(owl_str):
    """Return a BioPAX Model from an OWL string.

    Parameters
    ----------
    owl_str : str
        A OWL string of BioPAX content.

    Returns
    -------
    pybiopax.biopax.BioPaxModel
        A BioPAX Model deserialized from the OWL string.
    """
    return BioPaxModel.from_xml(ET.fromstring(owl_str))


def model_from_owl_file(fname):
    """Return a BioPAX Model from an OWL string.

    Parameters
    ----------
    fname : str
        A OWL file of BioPAX content.

    Returns
    -------
    pybiopax.biopax.BioPaxModel
        A BioPAX Model deserialized from the OWL file.
    """
    with open(fname, 'r') as fh:
        owl_str = fh.read()
        return model_from_owl_str(owl_str)


def model_from_owl_url(url):
    """Return a BioPAX Model from an URL pointing to an OWL file.

    Parameters
    ----------
    url : str
        A OWL URL with BioPAX content.

    Returns
    -------
    pybiopax.biopax.BioPaxModel
        A BioPAX Model deserialized from the OWL file.
    """
    res = requests.get(url)
    res.raise_for_status()
    return model_from_owl_str(res.text)


def model_to_owl_str(model):
    return xml_to_str(model.to_xml())


def model_to_owl_file(model, fname):
    xml_to_file(model.to_xml(), fname)
