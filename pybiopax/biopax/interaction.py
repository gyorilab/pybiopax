__all__ = ['Process', 'Interaction', 'GeneticInteraction',
           'MolecularInteraction', 'TemplateReaction',
           'Control', 'Conversion', 'Catalysis',
           'TemplateReactionRegulation', 'Modulation',
           'ComplexAssembly', 'BiochemicalReaction',
           'Degradation', 'Transport', 'TransportWithBiochemicalReaction']

from typing import ClassVar, List, Optional, TYPE_CHECKING
from .base import Entity
from .physical_entity import PhysicalEntity
from .util import Stoichiometry, DeltaG, KPrime


class Process(Entity):
    """BioPAX Process."""
    def __init__(self,
                 controlled_of: Optional = None,
                 step_process_of: Optional = None,
                 pathway_component_of: Optional = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.controlled_of = controlled_of
        self.step_process_of = step_process_of
        self.pathway_component_of = pathway_component_of


class Interaction(Process):
    """BioPAX Interaction."""
    list_types: ClassVar[List[str]] = Process.list_types + ['participant']

    def __init__(self,
                 participant: Optional = None,
                 interaction_type: Optional = None,
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
    list_types: ClassVar[List[str]] = Interaction.list_types + ['product']

    def __init__(self,
                 template: Optional = None,
                 product: Optional = None,
                 template_direction: Optional = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.template = template
        self.product = product
        self.template_direction = template_direction


class Control(Interaction):
    """BioPAX Control."""
    list_types: ClassVar[List[str]] = Interaction.list_types + ['controller']

    def __init__(self,
                 control_type: Optional = None,
                 controller: Optional = None,
                 controlled: Optional = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.control_type = control_type
        self.controller = controller
        self.controlled = controlled


class Conversion(Interaction):
    """BioPAX Conversion."""
    list_types: ClassVar[List[str]] = Interaction.list_types + \
        ['left', 'right', 'participant_stoichiometry']

    def __init__(self,
                 left: Optional[List[PhysicalEntity]] = None,
                 right: Optional[List[PhysicalEntity]] = None,
                 conversion_direction: Optional[List] = None,
                 participant_stoichiometry: Optional[List[Stoichiometry]] = None,
                 spontaneous: Optional[bool] = None,
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
                 catalysis_direction: Optional = None,
                 cofactor: Optional = None,
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
                 delta_s: Optional = None,
                 delta_h: Optional = None,
                 delta_g: Optional[List[DeltaG]] = None,
                 k_e_q: Optional[List[KPrime]] = None,
                 e_c_number: Optional[str] = None,
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

