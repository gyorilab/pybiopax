# -*- coding: utf-8 -*-

"""Tools for traversing the BioPAX data model."""

from typing import Any, Iterable, Set, Tuple

from .biopax import (
    BiochemicalReaction,
    BioPaxModel,
    Catalysis,
    ModificationFeature,
    PhysicalEntity,
    Protein,
    SimplePhysicalEntity,
)

__all__ = [
    "get_simple_physical_entity_xrefs",
    "is_modification_reaction",
    "iter_modification_reactions",
    "iter_modification_reactions",
    "iter_cofactored_catalyses",
]


def get_simple_physical_entity_xrefs(obj: SimplePhysicalEntity) -> Set[Tuple[str, str]]:
    """Get xrefs from a simple physical entity as pairs."""
    if not obj.entity_reference:
        return set()
    return {(xref.db, xref.id) for xref in obj.entity_reference.xref or []}


def is_modification_reaction(obj: Any) -> bool:
    """Check if the object is a biochemical reaction with the same
    entity as reactant/product but it's modified.
    """
    if not isinstance(obj, BiochemicalReaction):
        return False
    if len(obj.left) != 1 or len(obj.right) != 1:
        return False
    left, right = obj.left[0], obj.right[0]
    if not isinstance(left, Protein) or not isinstance(right, Protein):
        return False
    left_xrefs = get_simple_physical_entity_xrefs(left)
    right_xrefs = get_simple_physical_entity_xrefs(right)
    print(left_xrefs)
    print(right_xrefs)
    return 0 < len(left_xrefs.intersection(right_xrefs))


def iter_modification_reactions(model: BioPaxModel) -> Iterable[BiochemicalReaction]:
    """Iterate over biochemical reactions in the model that are modification reactions which
    pass :func:`is_modification_reaction`.
    """
    for obj in model.get_objects_by_type(BiochemicalReaction):
        if is_modification_reaction(obj):
            yield obj


def iter_cofactored_catalyses(model: BioPaxModel) -> Iterable[Catalysis]:
    """Iterate over catalyses of biochemical reactions that require a cofactor."""
    for obj in model.get_objects_by_type(Catalysis):
        if not obj.cofactor:
            continue
        if not isinstance(obj.controlled, BiochemicalReaction):
            continue
        yield obj


def iter_modifications(entity: PhysicalEntity, s: str) -> Iterable[ModificationFeature]:
    """Iterate over modification features in a protein that"""
    for feature in entity.feature or []:
        # If this is a modification feature which has a known type
        # and that type includes "phospho", i.e., is a phosphorylation
        if (
            isinstance(feature, ModificationFeature)
            and feature.modification_type
            and any(s in mod for mod in feature.modification_type.term)
        ):
            yield feature
