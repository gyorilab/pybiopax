from .base import Entity


class Interaction(Entity):
    def __init__(self,
                 participant=None,
                 interaction_type=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.participant = participant
        self.interaction_type = interaction_type


class GeneticInteraction(Interaction):
    pass


class MolecularInteraction(Interaction):
    pass


class TemplateReaction(Interaction):
    pass


class Control(Interaction):
    def __init__(self,
                 control_type=None,
                 pathway_controller=None,
                 pe_controller=None,
                 controlled=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.control_type = control_type,
        self.pathway_controller = pathway_controller
        self.pe_controller = pe_controller
        self.controlled = controlled


class Conversion(Interaction):
    def __init__(self,
                 left=None,
                 right=None,
                 conversion_direction=None,
                 participant_soichiometry=None,
                 spontaneous=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.left = left
        self.right = right
        self.conversion_direction = conversion_direction
        self.participant_stoichiometry = participant_soichiometry
        self.spontaneous = spontaneous


class Catalysis(Control):
    def __init__(self,
                 catalysis_direction=None,
                 cofactor=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.catalysis_direction = catalysis_direction
        self.cofactor = cofactor


class TemplateReactionRegulation(Control):
    pass


class Modulation(Control):
    pass


class Conversion(Interaction):
    pass


class ComplexAssembly(Conversion):
    pass


class BiochemicalReaction(Conversion):
    pass


class Degradation(Conversion):
    pass


class Transport(Conversion):
    pass


class TransportWithBiochemicalReaction(Conversion):
    pass


