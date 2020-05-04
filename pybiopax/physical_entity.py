from .base import Entity


class PhysicalEntity(Entity):
    list_types = ['feature', 'not_feature', 'member_physical_entity']

    def __init__(self,
                 feature=None,
                 not_feature=None,
                 controller_of=None,
                 component_of=None,
                 member_physical_entity_of=None,
                 member_physical_entity=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.feature = feature
        self.not_feature = not_feature
        self.controller_of = controller_of
        self.component_of = component_of
        self.member_physical_entity_of = member_physical_entity_of
        self.member_physical_entity = member_physical_entity


class Protein(PhysicalEntity):
    pass


class SmallMolecule(PhysicalEntity):
    pass


class Rna(PhysicalEntity):
    pass


class Complex(PhysicalEntity):
    list_types = ['component', 'component_stoichiometry']

    def __init__(self,
                 component=None,
                 component_stoichiometry=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.component = component
        self.component_stoichiometry = component_stoichiometry


class Dna(PhysicalEntity):
    pass