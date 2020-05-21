__all__ = ['model_from_owl_str', 'model_from_owl_file']


from xml.etree import ElementTree as ET
from .biopax.model import BioPaxModel


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
        return model_from_owl_file(owl_str)
