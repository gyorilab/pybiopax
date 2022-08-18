__all__ = ['PhysicalEntity', 'SimplePhysicalEntity', 'Protein',
           'SmallMolecule', 'Rna', 'Complex', 'Dna', 'DnaRegion',
           'RnaRegion']

from typing import List, Optional

from .base import Entity, Controller
from .util import EntityFeature, EntityReference


class PhysicalEntity(Entity, Controller):
    """BioPAX PhysicalEntity.

    Attributes
    ----------
    feature : List[EntityFeature]
    not_feature : List[EntityFeature]
    member_physical_entity : List[PhysicalEntity]
    cellular_location : CellularLocationVocabulary
    """
    list_types = Entity.list_types + \
        ['feature', 'not_feature', 'member_physical_entity']

    def __init__(self,
                 feature: Optional[List[EntityFeature]] = None,
                 not_feature=None,
                 member_physical_entity=None,
                 cellular_location=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.feature = feature if feature else []
        self.not_feature = not_feature if not_feature else []
        self.member_physical_entity = member_physical_entity if \
            member_physical_entity else []
        self.cellular_location = cellular_location
        self._component_of = set()
        self._member_physical_entity_of = set()

    @property
    def component_of(self):
        return self._component_of

    @property
    def member_physical_entity_of(self):
        return self._member_physical_entity_of

    def __str__(self):
        name = self.display_name if self.display_name else self.standard_name
        s = '%s(%s)' % (self.__class__.__name__, name)
        return s

    def __repr__(self):
        return str(self)


class SimplePhysicalEntity(PhysicalEntity):
    """BioPAX SimplePhysicalEntity.

    Attributes
    ----------
    entity_reference : EntityReference
    """
    def __init__(
        self,
        entity_reference: Optional[EntityReference] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.entity_reference = entity_reference


class Protein(SimplePhysicalEntity):
    """BioPAX Protein."""
    pass


class SmallMolecule(SimplePhysicalEntity):
    """BioPAX SmallMolecule."""
    pass


class Rna(SimplePhysicalEntity):
    """BioPAX Rna."""
    pass


class Complex(PhysicalEntity):
    """BioPAX Complex.

    Attributes
    ----------
    component : List[PhysicalEntity]
    component_stoichiometry : List[Stoichiometry]
    """
    list_types = PhysicalEntity.list_types + \
        ['component', 'component_stoichiometry']

    def __init__(self,
                 component: Optional[List[PhysicalEntity]] = None,
                 component_stoichiometry: Optional[List] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.component = component if component else []
        self.component_stoichiometry = component_stoichiometry if \
            component_stoichiometry else []


class Dna(SimplePhysicalEntity):
    """BioPAX Dna."""
    pass


class DnaRegion(SimplePhysicalEntity):
    """BioPAX DnaRegion"""
    pass


class RnaRegion(SimplePhysicalEntity):
    """BioPAX RnaRegion"""
    pass
