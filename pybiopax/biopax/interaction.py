__all__ = ['Process', 'Interaction', 'GeneticInteraction',
           'MolecularInteraction', 'TemplateReaction',
           'Control', 'Conversion', 'Catalysis',
           'TemplateReactionRegulation', 'Modulation',
           'ComplexAssembly', 'BiochemicalReaction',
           'Degradation', 'Transport', 'TransportWithBiochemicalReaction']

from .base import Entity


class Process(Entity):
    """BioPAX Process."""
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
    """BioPAX Interaction."""
    def __init__(self,
                 participant=None,
                 interaction_type=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.participant = participant
        self.interaction_type = interaction_type


class GeneticInteraction(Interaction):
    """BioPAX GeneticInteraction."""
    pass


class MolecularInteraction(Interaction):
    """BioPAX MolecularInteraction."""
    pass


class TemplateReaction(Interaction):
    """BioPAX TemplateReaction."""
    list_types = Interaction.list_types + ['product']

    def __init__(self,
                 template=None,
                 product=None,
                 template_direction=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.template = template
        self.product = product
        self.template_direction = template_direction


class Control(Interaction):
    """BioPAX Control."""
    list_types = Interaction.list_types + ['controller']

    def __init__(self,
                 control_type=None,
                 controller=None,
                 controlled=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.control_type = control_type
        self.controller = controller
        self.controlled = controlled


class Conversion(Interaction):
    """BioPAX Conversion."""
    list_types = Interaction.list_types + \
        ['left', 'right', 'participant_stoichiometry']

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
    """BioPAX Catalysis."""
    def __init__(self,
                 catalysis_direction=None,
                 cofactor=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.catalysis_direction = catalysis_direction
        self.cofactor = cofactor


class TemplateReactionRegulation(Control):
    """BioPAX TemplateReactionRegulation."""
    pass


class Modulation(Control):
    """BioPAX Modulation."""
    pass


class ComplexAssembly(Conversion):
    """BioPAX ComplexAssembly."""
    pass


class BiochemicalReaction(Conversion):
    """BioPAX BiochemicalReaction."""
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
    """BioPAX Degradation."""
    pass


class Transport(Conversion):
    """BioPAX Transport."""
    pass


class TransportWithBiochemicalReaction(BiochemicalReaction):
    """BioPAX TransportWithBiochemicalReaction."""
    pass

