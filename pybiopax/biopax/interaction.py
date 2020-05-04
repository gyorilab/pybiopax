__all__ = ['Process', 'Interaction', 'GeneticInteraction',
           'MolecularInteraction', 'TemplateReaction',
           'Control', 'Conversion', 'Catalysis',
           'TemplateReactionRegulation', 'Modulation',
           'ComplexAssembly', 'BiochemicalReaction',
           'Degradation', 'Transport', 'TransportWithBiochemicalReaction']

from .base import Entity


class Process(Entity):
    def __init__(self,
                 controlled_of=None,
                 step_process_of=None,
                 pathway_component_of=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.controlled_of = controlled_of
        self.step_process_of = step_process_of
        self.pathway_component_of = pathway_component_of


class Interaction(Process):
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
    list_types = ['controller']

    def __init__(self,
                 control_type=None,
                 controller=None,
                 controlled=None,
                 **kwargs):
        super().__init__(**kwargs)
        from .physical_entity import PhysicalEntity
        from .base import Pathway
        self.control_type = control_type
        self.pathway_controller = []
        self.pe_controller = []
        for contr in controller if controller else []:
            if isinstance(contr, Pathway):
                self.pathway_controller.append(contr)
            elif isinstance(contr, PhysicalEntity):
                self.pe_controller.append(contr)
        self.controlled = controlled


class Conversion(Interaction):
    list_types = ['left', 'right', 'participant_stoichiometry']

    def __init__(self,
                 left=None,
                 right=None,
                 conversion_direction=None,
                 participant_stoichiometry=None,
                 spontaneous=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.left = left
        self.right = right
        self.conversion_direction = conversion_direction
        self.participant_stoichiometry = participant_stoichiometry
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


class ComplexAssembly(Conversion):
    pass


class BiochemicalReaction(Conversion):
    def __init__(self,
                 delta_s=None,
                 delta_h=None,
                 delta_g=None,
                 k_e_q=None,
                 e_c_number=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.delta_s = delta_s
        self.delta_h = delta_h
        self.delta_g = delta_g
        self.k_e_q = k_e_q
        self.e_c_number = e_c_number


class Degradation(Conversion):
    pass


class Transport(Conversion):
    pass


class TransportWithBiochemicalReaction(Conversion):
    pass


