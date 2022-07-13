from collections import Counter
from typing import List, Mapping, Set, Tuple
from .biopax import BioPaxModel, Xref


def get_prefix_id_pairs(model: BioPaxModel) -> List[Tuple[str, str]]:
    """Return a list of database/identifier pairs used in the references of
    a BioPAX Model.

    Parameters
    ----------
    model :
        A BioPAX Model.

    Returns
    -------
    :
        A list of database/identifier pairs used in the model.
    """
    refs = list(model.get_objects_by_type(Xref))
    return [(ref.db, ref.id) for ref in refs]


def get_all_prefixes(model: BioPaxModel) -> Set[str]:
    """Return a set of all prefixes used in the references of a BioPAX Model.

    Parameters
    ----------
    model :
        A BioPAX Model.

    Returns
    -------
    :
        A set of all prefixes used in the model.
    """
    return {db for db, identifier in get_prefix_id_pairs(model)}


def get_prefix_statistics(model: BioPaxModel) -> Mapping[str, int]:
    """Return a dict of prefixes and the number of times they are used in
     references in a BioPAX Model.

    Parameters
    ----------
    model :
        A BioPAX Model.

    Returns
    -------
    :
        A dict of prefixes and the number of times they are used
        in references in the model.
     """
    return dict(Counter([db for db, identifier
                         in get_prefix_id_pairs(model)]).most_common())


