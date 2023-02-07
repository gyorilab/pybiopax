__all__ = ['model_from_owl_str', 'model_from_owl_file', 'model_to_owl_str',
           'model_to_owl_file', 'model_from_owl_url', 'model_from_pc_query',
           'model_from_reactome', 'model_from_ecocyc', 'model_from_metacyc',
           'model_from_biocyc', 'model_from_humancyc', 'model_from_netpath',
           'model_from_owl_gz', 'PYBIOPAX_TQDM_CONFIG'
           ]

import gzip
import os
import pathlib

import requests
from lxml import etree
from typing import Any, Mapping, Optional, Union
from .biopax.model import BioPaxModel, PYBIOPAX_TQDM_CONFIG
from .xml_util import xml_to_str, xml_to_file
from .pc_client import graph_query


def model_from_owl_str(owl_str: str) -> BioPaxModel:
    """Return a BioPAX Model from an OWL string.

    Parameters
    ----------
    owl_str :
        A OWL string of BioPAX content.

    Returns
    -------
    pybiopax.biopax.BioPaxModel
        A BioPAX Model deserialized from the OWL string.
    """
    return BioPaxModel.from_xml(etree.fromstring(owl_str.encode('utf-8')))


def model_from_owl_file(fname: Union[str, pathlib.Path, os.PathLike],
                        encoding: Optional[str] = None) \
        -> BioPaxModel:
    """Return a BioPAX Model from an OWL string.

    Parameters
    ----------
    fname :
        A path to an OWL file of BioPAX content.
    encoding :
        The encoding type to be passed to :func:`open`.

    Returns
    -------
    :
        A BioPAX Model deserialized from the OWL file.
    """
    with open(fname, 'r', encoding=encoding) as fh:
        owl_str = fh.read()
        return model_from_owl_str(owl_str)


def model_from_owl_gz(path: Union[str, pathlib.Path, os.PathLike]) \
        -> BioPaxModel:
    """Return a BioPAX Model from an OWL file (gzipped).

    Parameters
    ----------
    path :
        A path to a gzipped OWL file of BioPAX content.

    Returns
    -------
    :
        A BioPAX Model deserialized from the OWL file.
    """
    with gzip.open(path, 'rt') as fh:
        return BioPaxModel.from_xml(etree.parse(fh).getroot())


def model_from_owl_gz_str(owl_gz_str: bytes) -> BioPaxModel:
    """Return a BioPAX Model from an OWL string.

    Parameters
    ----------
    owl_gz_str :
        A OWL string of BioPAX content.

    Returns
    -------
    pybiopax.biopax.BioPaxModel
        A BioPAX Model deserialized from the OWL string.
    """
    return model_from_owl_str(gzip.decompress(owl_gz_str).decode('utf-8'))


def model_from_owl_url(url: str,
                       request_params: Optional[Mapping[str, Any]] = None) \
        -> BioPaxModel:
    """Return a BioPAX Model from an URL pointing to an OWL file.

    Parameters
    ----------
    url :
        A OWL URL with BioPAX content.
    request_params :
        Additional keyword arguments to pass to :func:`requests.get`

    Returns
    -------
    :
        A BioPAX Model deserialized from the OWL file.
    """
    request_params = {} if not request_params else request_params
    res = requests.get(url, **request_params)
    res.raise_for_status()
    if url.endswith('gz'):
        return model_from_owl_gz_str(res.content)
    else:
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


def model_from_netpath(identifier: str) -> BioPaxModel:
    """Return a BioPAX model from a `NetPath <http://netpath.org>`_ entry.

    Parameters
    ----------
    identifier :
        The NetPath identifier for a pathway (e.g., ``22`` for the `leptin
        signaling pathway <http://netpath.org/pathways?path_id=NetPath_22>`_

    Returns
    -------
    :
        A BioPAX model obtained from the NetPath resource.
    """
    url = f"http://netpath.org/data/biopax/NetPath_{identifier}.owl"
    return model_from_owl_url(url)


def model_from_reactome(identifier: str) -> BioPaxModel:
    """Return a BioPAX model from a Reactome entry (pathway, event, etc.).

    Parameters
    ----------
    identifier :
        The Reactome identifier for a pathway (e.g., ``177929`` for `Signaling
        by EGFR <https://reactome.org/content/detail/R-HSA-177929>`_)
        or reaction (e.g., ``177946`` for `Pro-EGF is cleaved to form mature
        EGF <https://reactome.org/content/detail/R-HSA-177946>`_). For human
        pathways, the identifier for the BioPAX download is the same as the part
        that comes after ``R-HSA-``. For non-human pathways, this is not so
        clear.

    Returns
    -------
    :
        A BioPAX model obtained from the Reactome resource.
    """
    if identifier.startswith("R-HSA-"):
        # If you give something like R-XXX-YYYYY, just get the YYYYY part back
        # for download.
        identifier = identifier[len("R-HSA-"):]
    url = f"https://reactome.org/ReactomeRESTfulAPI/RESTfulWS/biopaxExporter/" \
          f"Level3/{identifier}"
    return model_from_owl_url(url)


def model_from_humancyc(identifier: str) -> BioPaxModel:
    """Return a BioPAX model from a HumanCyc entry.

    Parameters
    ----------
    identifier :
        The HumanCyc identifier for a pathway (e.g., ``PWY66-398`` for
        `TCA cycle
        <https://humancyc.org/HUMAN/NEW-IMAGE?type=PATHWAY&object=PWY66-398>`_)

    Returns
    -------
    :
        A BioPAX model obtained from the HumanCyc pathway.
    """
    return _model_from_xcyc("https://humancyc.org/HUMAN/pathway-biopax",
                            identifier)


def model_from_biocyc(identifier: str) -> BioPaxModel:
    """Return a BioPAX model from a `BioCyc <https://biocyc.org>`_ entry.

    BioCyc contains pathways for model eukaryotes and microbes.

    Parameters
    ----------
    identifier :
        The BioCyc identifier for a pathway (e.g., ``P105-PWY`` for
        `TCA cycle IV
        (2-oxoglutarate decarboxylase) <https://biocyc.org/META/NEW-IMAGE?
        type=PATHWAY&object=P105-PWY>`_)

    Returns
    -------
    :
        A BioPAX model obtained from the BioCyc pathway.
    """
    return _model_from_xcyc("https://biocyc.org/META/pathway-biopax",
                            identifier)


def model_from_metacyc(identifier: str) -> BioPaxModel:
    """Return a BioPAX model from a `MetaCyc <https://metacyc.org/>`_ entry.

    MetaCyc contains pathways for all organisms

    Parameters
    ----------
    identifier :
        The MetaCyc identifier for a pathway (e.g., ``TCA`` for
        `TCA cycle I (prokaryotic) <https://metacyc.org/META/NEW-IMAGE?type=PATHWAY&object=TCA>`_)

    Returns
    -------
    :
        A BioPAX model obtained from the MetaCyc pathway.
    """
    return _model_from_xcyc("https://metacyc.org/META/pathway-biopax",
                            identifier)


def model_from_ecocyc(identifier: str) -> BioPaxModel:
    """Return a BioPAX model from a `EcoCyc <https://ecocyc.org/>`_ entry.

    EcoCyc contains pathways for Escherichia coli K-12 MG1655.

    Parameters
    ----------
    identifier :
        The EcoCyc identifier for a pathway (e.g., ``TCA`` for
        `TCA cycle I (prokaryotic) <https://ecocyc.org/ECOLI/NEW-IMAGE?type=PATHWAY&object=TCA>`_)

    Returns
    -------
    :
        A BioPAX model obtained from the EcoCyc pathway.
    """
    return _model_from_xcyc("https://ecocyc.org/ECOLI/pathway-biopax",
                            identifier)


def _model_from_xcyc(url: str, identifier: str) -> BioPaxModel:
    """Return a BioPAX model from one of the Cyc databases entry.

    Parameters
    ----------
    url :
        The base url for the XXXCyc BioPAX download endpoint. All of them have
        the form ``https://....../META/pathway-biopax``.
    identifier :
        The site-specific identifier for a pathway

    Returns
    -------
    :
        A BioPAX model obtained from the pathway.
    """
    # Extend URL with arguments
    url = url + f'?type=3&object={identifier}'
    # Not sure if the SSL issue is temporary. Remove verify=False later
    return model_from_owl_url(url, request_params={'verify': False})


def model_to_owl_str(model: BioPaxModel) -> str:
    """Return an OWL string serialized from a BioPaxModel object.

    Parameters
    ----------
    model :
        The BioPaxModel to serialize into an OWL string.

    Returns
    -------
    :
        The OWL string for the model.
    """
    return xml_to_str(model.to_xml())


def model_to_owl_file(model: BioPaxModel,
                      fname: Union[str, pathlib.Path, os.PathLike]):
    """Write an OWL string serialized from a BioPaxModel object into a file.

    Parameters
    ----------
    model :
        The BioPaxModel to serialize into an OWL file.
    fname :
        The path to the target OWL file.
    """
    xml_to_file(model.to_xml(), fname)
