"""A client to the PathwayCommons REST API. For more details about
the service, see the documentation at https://www.pathwaycommons.org/pc2/."""
__all__ = ['graph_query']

import logging
import requests

logger = logging.getLogger(__name__)
pc2_url = 'http://www.pathwaycommons.org/pc2/'


def graph_query(kind, source, target=None, **query_params):
    """Perform a graph query on PathwayCommons.

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
    str
        A BioPAX OWL string that can then be deserialized into a BioPaxModel.
    """

    params = {}
    params['format'] = 'BIOPAX'
    params['organism'] = query_params.get('organism', '9606')
    params['datasource'] = query_params.get('datasource', None)
    # Get the "kind" string
    kind_str = kind.lower()
    if kind not in ['neighborhood', 'pathsbetween', 'pathsfromto']:
        raise ValueError('Invalid query type %s' % kind_str)
    params['kind'] = kind_str
    # Get the source string
    params['source'] = _get_query_entity(source)
    try:
        params['limit'] = int(query_params.get('limit', 1))
    except (TypeError, ValueError):
        raise ValueError('Invalid neighborhood limit %s' %
                         query_params.get('limit'))
    if kind == 'pathsfromto':
        params['target'] = _get_query_entity(target)

    logger.info('Sending Pathway Commons query with parameters: ')
    for k, v in params.items():
        logger.info(' %s: %s' % (k, v))

    res = requests.get(pc2_url + 'graph', params=params)
    if not res.status_code == 200:
        logger.error('Response is HTTP code %d.' % res.status_code)
        if res.status_code == 500:
            logger.error('Note: HTTP code 500 can mean empty '
                         'results for a valid query.')
        return None
    return res.text


def _get_query_entity(ent):
    if isinstance(ent, str):
        return ent
    elif isinstance(ent, (list, tuple)):
        return ','.join(ent)
    else:
        raise ValueError('Invalid query entity: %s' % str(ent))
