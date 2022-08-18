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
                 **kwargs):
        super().__init__(**kwargs)
        self._controlled_of = set()
        self._step_process_of = set()
        self._pathway_component_of = set()

    @property
    def controlled_of(self):
        return self._controlled_of

    @property
    def step_process_of(self):
        return self._step_process_of

    @property
    def pathway_component_of(self):
        return self._pathway_component_of


class Interaction(Process):
    """BioPAX Interaction.

    Attributes
    ----------
    participant : List[Entity]
    interaction_type : List[str]
    """
    list_types = Process.list_types + ['participant', 'interaction_type']

    def __init__(self,
                 participant=None,
                 interaction_type=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.participant = participant if participant else []
        self.interaction_type = interaction_type if interaction_type else []


class GeneticInteraction(Interaction):
    """BioPAX GeneticInteraction."""
    pass


class MolecularInteraction(Interaction):
    """BioPAX MolecularInteraction."""
    pass


class TemplateReaction(Interaction):
    """BioPAX TemplateReaction.

    Attributes
    ----------
    template : NucleicAcid
    product : List[PhysicalEntity]
    template_direction : str
    """
    list_types = Interaction.list_types + ['product']

    def __init__(self,
                 template=None,
                 product=None,
                 template_direction=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.template = template
        self.product = product if product else []
        self.template_direction = template_direction


class Control(Interaction):
    """BioPAX Control.

    Attributes
    ----------
    control_type : str
    controller : List[Process]
    controlled : Process
    """
    list_types = Interaction.list_types + ['controller']

    def __init__(self,
                 control_type=None,
                 controller=None,
                 controlled=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.control_type = control_type
        self.controller = controller if controller else []
        self.controlled = controlled


class Conversion(Interaction):
    """BioPAX Conversion.

    Attributes
    ----------
    left : List[PhysicalEntity]
    right : List[PhysicalEntity]
    conversion_direction : str
    participant_stoichiometry : List[Stoichiometry]
    spontaneous : bool
    """
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
        self.left = left if left else []
        self.right = right if right else []
        self.conversion_direction = conversion_direction
        self.participant_stoichiometry = participant_stoichiometry  if \
            participant_stoichiometry else []
        self.spontaneous = spontaneous


class Catalysis(Control):
    """BioPAX Catalysis.

    Attributes
    ----------
    catalysis_direction : str
    cofactor : List[PhysicalEntity]
    """
    list_types = Control.list_types + ['cofactor']

    def __init__(self,
                 catalysis_direction=None,
                 cofactor=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.catalysis_direction = catalysis_direction
        self.cofactor = cofactor if cofactor else []


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
    """BioPAX BiochemicalReaction.

    Attributes
    ----------
    delta_s : List[float]
    delta_h : List[float]
    delta_g : List[DeltaG]
    k_e_q : List[KPrime]
    e_c_number : List[str]
    """
    list_types = Conversion.list_types + ['delta_s', 'delta_h', 'delta_g',
                                          'k_e_q', 'e_c_number']

    def __init__(self,
                 delta_s=None,
                 delta_h=None,
                 delta_g=None,
                 k_e_q=None,
                 e_c_number=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.delta_s = delta_s if delta_s else []
        self.delta_h = delta_h if delta_h else []
        self.delta_g = delta_g if delta_g else []
        self.k_e_q = k_e_q if k_e_q else []
        self.e_c_number = e_c_number if e_c_number else []


class Degradation(Conversion):
    """BioPAX Degradation."""
    pass


class Transport(Conversion):
    """BioPAX Transport."""
    pass


class TransportWithBiochemicalReaction(BiochemicalReaction):
    """BioPAX TransportWithBiochemicalReaction."""
    pass

