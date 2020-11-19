__all__ = ['model_from_owl_str', 'model_from_owl_file', 'model_to_owl_str',
           'model_to_owl_file', 'model_from_owl_url', 'model_from_pc_query']

import requests
from lxml import etree
from .biopax.model import BioPaxModel
from .xml_util import xml_to_str, xml_to_file
from .pc_client import graph_query


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
    return BioPaxModel.from_xml(etree.fromstring(owl_str.encode('utf-8')))


def model_from_owl_file(fname, encoding=None):
    """Return a BioPAX Model from an OWL string.

    Parameters
    ----------
    fname : str
        A OWL file of BioPAX content.
    encoding : Optional[str]
        The encoding type to be passed to :func:`open`.

    Returns
    -------
    pybiopax.biopax.BioPaxModel
        A BioPAX Model deserialized from the OWL file.
    """
    with open(fname, 'r', encoding=encoding) as fh:
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


def model_from_pc_query(kind, source, target=None, **query_params):
    """Return a BioPAX Model from a Pathway Commons query.

    For more information on these queries, see
    http://www.pathwaycommons.org/pc2/#graph

    Parameters
    ----------
    kind : str
        The kind of graph query to perform. Currently 3 options are
        implemented, 'neighborhood', 'pathsbetween' and 'pathsfromto'.
    source : list[str]
        A single gene name or a list of gene names which are the source set for
        the graph query.
    target : Optional[list[str]]
        A single gene name or a list of gene names which are the target set for
        the graph query. Only needed for 'pathsfromto' queries.
    limit : Optional[int]
        This limits the length of the longest path considered in
        the graph query. Default: 1
    organism : Optional[str]
        The organism used for the query. Default: '9606' corresponding
        to human.
    datasource : Optional[list[str]]
        A list of database sources that the query results should include.
        Example: ['pid', 'panther']. By default, all databases are considered.

    Returns
    -------
    pybiopax.biopax.BioPaxModel
        A BioPAX Model obtained from the results of the Pathway Commons query.
    """
    owl_str = graph_query(kind, source, target=target, **query_params)
    return model_from_owl_str(owl_str)


def model_to_owl_str(model):
    """Return an OWL string serialized from a BioPaxModel object.

    Parameters
    ----------
    model : pybiopax.biopax.BioPaxModel
        The BioPaxModel to serialize into an OWL string.

    Returns
    -------
    str
        The OWL string for the model.
    """
    return xml_to_str(model.to_xml())


def model_to_owl_file(model, fname):
    """Write an OWL string serialized from a BioPaxModel object into a file.

    Parameters
    ----------
    model : pybiopax.biopax.BioPaxModel
        The BioPaxModel to serialize into an OWL file.
    fname : str
        The path to the target OWL file.
    """
    xml_to_file(model.to_xml(), fname)
