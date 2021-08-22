__all__ = ['PhysicalEntity', 'SimplePhysicalEntity', 'Protein',
           'SmallMolecule', 'Rna', 'Complex', 'Dna', 'DnaRegion',
           'RnaRegion']

from typing import ClassVar, List, Optional

from .base import Entity


class PhysicalEntity(Entity):
    """BioPAX PhysicalEntity."""
    list_types: ClassVar[List[str]] = Entity.list_types + \
        ['feature', 'not_feature', 'member_physical_entity']

    def __init__(self,
                 feature: Optional = None,
                 not_feature: Optional = None,
                 controller_of: Optional = None,
                 component_of: Optional = None,
                 member_physical_entity_of: Optional = None,
                 member_physical_entity: Optional = None,
                 cellular_location: Optional = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.feature = feature
        self.not_feature = not_feature
        self.controller_of = controller_of
        self.component_of = component_of
        self.member_physical_entity_of = member_physical_entity_of
        self.member_physical_entity = member_physical_entity
        self.cellular_location = cellular_location

    def __str__(self) -> str:
        s = '%s(%s)' % (self.__class__.__name__,
                        self.display_name)
        return s

    def __repr__(self) -> str:
        return str(self)


class SimplePhysicalEntity(PhysicalEntity):
    """BioPAX SimplePhysicalEntity."""
    def __init__(self,
                 entity_reference: Optional = None,
                 **kwargs):
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
    """BioPAX Complex."""
    list_types: ClassVar[List[str]] = PhysicalEntity.list_types + \
        ['component', 'component_stoichiometry']

    def __init__(self,
                 component: Optional = None,
                 component_stoichiometry: Optional = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.component = component
        self.component_stoichiometry = component_stoichiometry


class Dna(SimplePhysicalEntity):
    """BioPAX Dna."""
    pass


class DnaRegion(SimplePhysicalEntity):
    """BioPAX DnaRegion"""
    pass


class RnaRegion(SimplePhysicalEntity):
    """BioPAX RnaRegion"""
    pass
