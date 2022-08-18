__all__ = ['BindingFeature', 'BioSource', 'BiochemicalPathwayStep',
           'CellVocabulary', 'CellularLocationVocabulary', 'ChemicalConstant',
           'ChemicalStructure', 'ControlledVocabulary', 'DeltaG',
           'DnaReference', 'DnaRegionReference', 'EntityFeature',
           'EntityReference', 'EntityReferenceTypeVocabulary', 'Evidence',
           'EvidenceCodeVocabulary', 'ExperimentalForm',
           'ExperimentalFormVocabulary', 'FragmentFeature',
           'InteractionVocabulary', 'KPrime', 'ModificationFeature',
           'NucleicAcidReference', 'NucleicAcidRegionReference',
           'PathwayStep', 'PhenotypeVocabulary', 'ProteinReference',
           'Provenance', 'PublicationXref', 'RelationshipTypeVocabulary',
           'RelationshipXref', 'RnaReference', 'RnaRegionReference', 'Score',
           'SequenceEntityReference', 'SequenceInterval', 'SequenceLocation',
           'SequenceModificationVocabulary', 'SequenceRegionVocabulary',
           'SequenceSite', 'SmallMoleculeReference', 'Stoichiometry',
           'TissueVocabulary', 'UnificationXref', 'UtilityClass', 'Xref']

from typing import List, Optional

from .base import BioPaxObject, Named, Observable, XReferrable


class UtilityClass(BioPaxObject):
    """BioPAX UtilityClass."""
    def __int__(self, **kwargs):
        super().__init__(**kwargs)


class Evidence(UtilityClass, XReferrable):
    """BioPAX Evidence.

    Attributes
    ----------
    confidence : List[Score]
    evidence_code : List[EvidenceCodeVocabulary]
    experimental_form : List[ExperimentalForm]
    """
    list_types = UtilityClass.list_types + XReferrable.list_types

    def __init__(self,
                 confidence=None,
                 evidence_code=None,
                 experimental_form=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.confidence = confidence
        self.evidence_code = evidence_code
        self.experimental_form = experimental_form


class Provenance(UtilityClass, Named):
    """BioPAX Provenance."""
    list_types = Named.list_types

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class EntityFeature(UtilityClass, Observable):
    """BioPAX UtilityClass.

    Attributes
    ----------
    owner_entity_reference : EntityReference
    feature_location : SequenceLocation
    member_feature : List[EntityFeature]
    feature_location_type : SequenceRegionVocabulary
    """
    list_types = UtilityClass.list_types + Observable.list_types

    def __init__(self,
                 owner_entity_reference=None,
                 feature_location=None,
                 member_feature=None,
                 feature_location_type=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.owner_entity_reference = owner_entity_reference
        self.feature_location = feature_location
        self.member_feature = member_feature
        self.feature_location_type = feature_location_type
        self._feature_of = set()
        self._not_feature_of = set()
        self._entity_feature_of = set()
        self._member_feature_of = set()

    @property
    def feature_of(self):
        return self._feature_of

    @property
    def not_feature_of(self):
        return self._not_feature_of

    @property
    def entity_feature_of(self):
        return self._entity_feature_of

    @property
    def member_feature_of(self):
        return self._member_feature_of


class ModificationFeature(EntityFeature):
    """BioPAX ModificationFeature.

    Attributes
    ----------
    modification_type : SequenceModificationVocabulary
    """

    def __init__(
        self,
        modification_type=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.modification_type = modification_type

    def __str__(self):
        return '%s(%s%s)' % (self.__class__.__name__,
                             self.modification_type if self.modification_type
                             else '',
                             '@%s' % self.feature_location
                             if self.feature_location else '')

    def __repr__(self):
        return str(self)


class FragmentFeature(EntityFeature):
    """BioPAX FragmentFeature."""
    pass


class BindingFeature(EntityFeature):
    """BioPAX BindingFeature.

    Attributes
    ----------
    binds_to : BindingFeature
    intra_molecular : bool
    """
    def __init__(self,
                 binds_to=None,
                 intra_molecular=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.binds_to = binds_to
        self.intra_molecular = intra_molecular


class ChemicalConstant(UtilityClass):
    """BioPAX ChemicalConstant.

    Attributes
    ----------
    ionic_strength : float
    ph : float
    p_mg : float
    temperature : float
    """
    xml_types = {'ionic_strength': 'float',
                 'ph': 'float',
                 'p_mg': 'float',
                 'temperature': 'float'}

    def __init__(self,
                 ionic_strength=None,
                 ph=None,
                 p_mg=None,
                 tempterature=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.ionic_strength = ionic_strength
        self.ph = ph
        self.p_mg = p_mg
        self.temperature = tempterature


class DeltaG(ChemicalConstant):
    """BioPAX DeltaG.

    Attributes
    ----------
    delta_g_prime : float
    """
    xml_types = {'delta_g_prime0': 'float'}

    def __init__(self,
                 delta_g_prime0=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.delta_g_prime0 = delta_g_prime0


class KPrime(ChemicalConstant):
    """BioPAX KPrime.

    Attributes
    ----------
    k_prime : float
    """
    xml_types = {'k_prime': 'float'}

    def __init__(self, k_prime, **kwargs):
        super().__init__(**kwargs)
        self.k_prime = k_prime


class ChemicalStructure(UtilityClass):
    """BioPAX ChemicalStructure.

    Attributes
    ----------
    structure_format : str
    structure_data : str
    """
    def __init__(self,
                 structure_format=None,
                 structure_data=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.structure_format = structure_format
        self.structure_data = structure_data


class BioSource(UtilityClass, Named):
    """BioPAX BioSource.

    Attributes
    ----------
    cell_type : CellVocabulary
    tissue : TissueVocabulary
    """
    list_types = Named.list_types

    def __init__(self,
                 cell_type=None,
                 tissue=None,
                 taxon_xref=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.cell_type = cell_type
        self.tissue = tissue
        self.taxon_xref = taxon_xref


class ExperimentalForm(UtilityClass):
    """BioPAX ExperimentalForm.

    Attributes
    ----------
    experimental_form_entity : Entity
    experimental_form_description : List[ExperimentalFormVocabulary]
    experimental_feature : List[EntityFeature]
    """
    def __init__(self,
                 experimental_form_entity=None,
                 experimental_form_description=None,
                 experimental_feature=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.experimental_form_entity = experimental_form_entity
        self.experimental_form_description = experimental_form_description
        self.experimental_feature = experimental_feature


class SequenceLocation(UtilityClass):
    """BioPAX SequenceLocation.

    Attributes
    ----------
    region_type : List[SequenceRegionVocabulary]
    """
    def __init__(self,
                 region_type=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.region_type = region_type


class SequenceInterval(SequenceLocation):
    """BioPAX SequenceInterval.

    Attributes
    ----------
    sequence_interval_begin : SequenceSite
    sequence_interval_end : SequenceSite
    """
    def __init__(self,
                 sequence_interval_begin=None,
                 sequence_interval_end=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.sequence_interval_begin = sequence_interval_begin
        self.sequence_interval_end = sequence_interval_end

    def __str__(self):
        return '%s(%s-%s)' % (self.__class__.__name__,
                              self.sequence_interval_begin,
                              self.sequence_interval_end)

    def __repr__(self):
        return str(self)


class SequenceSite(SequenceLocation):
    """BioPAX SequenceSite.

    Attributes
    ----------
    position_status : str
    sequence_position : int
    """
    xml_types = {'sequence_position': 'int'}

    def __init__(self,
                 position_status=None,
                 sequence_position=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.position_status = position_status
        self.sequence_position = sequence_position

    def __str__(self):
        return '%s(%s)' % (self.__class__.__name__,
                           self.sequence_position)

    def __repr__(self):
        return str(self)


class PathwayStep(UtilityClass, Observable):
    """BioPAX PathwayStep.

    Attributes
    ----------
    step_process : List[Process]
    next_step : List[Process]
    """
    list_types = UtilityClass.list_types + Observable.list_types

    def __init__(self,
                 step_process=None,
                 next_step=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.step_process = step_process
        self.next_step = next_step
        self._next_step_of = set()
        self._pathway_order_of = set()

    @property
    def next_step_of(self):
        return self._next_step_of

    @property
    def pathway_order_of(self):
        return self._pathway_order_of


class BiochemicalPathwayStep(PathwayStep):
    """BioPAX BiochemicalPathwayStep.

    Attributes
    ----------
    step_conversion : Conversion
    step_direction : str
    """
    def __init__(self,
                 step_conversion=None,
                 step_direction=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.step_conversion = step_conversion
        self.step_direction = step_direction


class Xref(UtilityClass):
    """BioPAX Xref.

    Attributes
    ----------
    db : str
    id : str
    db_version : str
    id_version : str
    """
    def __init__(self,
                 db=None,
                 id=None,
                 db_version=None,
                 id_version=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.db_version = db_version
        self.id_version = id_version
        self.id = id
        self._xref_of = set()

    @property
    def xref_of(self):
        return self._xref_of


class PublicationXref(Xref):
    """BioPAX PublicationXref.

    Attributes
    ----------
    title : str
    url : List[str]
    source : List[str]
    author : List[str]
    year : int
    """
    list_types = Xref.list_types + ['url', 'source', 'author']
    xml_types = {'year': 'int'}

    def __init__(self,
                 title=None,
                 url=None,
                 source=None,
                 author=None,
                 year=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.url = url if url else []
        self.source = source if source else []
        self.author = author if author else []
        self.year = year


class UnificationXref(Xref):
    """BioPAX UnificationXref."""
    pass


class RelationshipXref(Xref):
    """BioPAX RelationshipXref.

    Attributes
    ----------
    relationship_type : RelationshipTypeVocabulary
    """
    def __init__(self,
                 relationship_type=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.relationship_type = relationship_type


class Score(UtilityClass, XReferrable):
    """BioPAX Score.

    Attributes
    ----------
    score_source : Provenance
    value : str
    """
    list_types = XReferrable.list_types

    def __init__(self,
                 score_source=None,
                 value=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.score_source = score_source
        self.value = value


class EntityReference(UtilityClass, Named, Observable):
    """BioPAX EntityReference.

    Attributes
    ----------
    entity_feature : List[EntityFeature]
    entity_reference_type : List[EntityReferenceTypeVocabulary]
    member_entity_reference : List[EntityReference]
    owner_entity_reference : List[EntityReference]
    """
    list_types = UtilityClass.list_types + Named.list_types + \
        Observable.list_types + ['entity_feature', 'member_entity_reference',
                                 'owner_entity_reference']

    def __init__(self,
                 entity_feature=None,
                 entity_reference_type=None,
                 member_entity_reference=None,
                 owner_entity_reference=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.entity_feature = entity_feature if entity_feature else []
        self.entity_reference_type = entity_reference_type
        self.member_entity_reference = member_entity_reference if \
            member_entity_reference else []
        self.owner_entity_reference = owner_entity_reference if \
            owner_entity_reference else []
        self._entity_reference_of = set()
        self._member_entity_reference_of = set()

    @property
    def entity_reference_of(self):
        return self._entity_reference_of

    @property
    def member_entity_reference_of(self):
        return self._member_entity_reference_of


class SequenceEntityReference(EntityReference):
    """BioPAX SequenceEntityReference.

    Attributes
    ----------
    organism : BioSource
    sequence : str
    """
    def __init__(self,
                 organism=None,
                 sequence=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.organism = organism
        self.sequence = sequence


class NucleicAcidReference(SequenceEntityReference):
    """BioPAX NucleicAcidReference"""
    pass


class NucleicAcidRegionReference(NucleicAcidReference):
    """BioPAX NucleicAcidRegionReference"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._subregion_of = set()

    @property
    def subregion_of(self):
        return self._subregion_of


class RnaReference(NucleicAcidReference):
    """BioPAX RnaReference."""
    pass


class RnaRegionReference(NucleicAcidRegionReference):
    """BioPAX RnaRegionReference."""
    pass


class ProteinReference(SequenceEntityReference):
    """BioPAX ProteinReference."""
    pass


class SmallMoleculeReference(EntityReference):
    """BioPAX SmallMoleculeReference.

    Attributes
    ----------
    structure : ChemicalStructure
    chemical_formula : str
    molecular_weight : float
    """
    xml_types = {'molecular_weight': 'float'}

    def __init__(self,
                 structure=None,
                 chemical_formula=None,
                 molecular_weight=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.structure = structure
        self.chemical_formula = chemical_formula
        self.molecular_weight = molecular_weight


class DnaReference(NucleicAcidReference):
    """BioPAX DnaReference."""
    pass


class DnaRegionReference(NucleicAcidRegionReference):
    """BioPAX DnaRegionReference."""
    pass


class Stoichiometry(UtilityClass):
    """BioPAX Stoichiometry.

    Attributes
    ----------
    stoichiometric_coefficient : float
    physical_entity : PhysicalEntity
    """
    xml_types = {'stoichiometric_coefficient': 'float'}

    def __init__(self,
                 stoichiometric_coefficient=None,
                 physical_entity=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.stoichiometric_coefficient = stoichiometric_coefficient
        self.physical_entity = physical_entity


class ControlledVocabulary(UtilityClass, XReferrable):
    """BioPAX ControlledVocabulary.

    Attributes
    ----------
    term : List[str]
    """
    list_types = UtilityClass.list_types + XReferrable.list_types + ['term']

    def __init__(self, term: List[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.term = term if term else []

    def __str__(self):
        if self.term:
            terms_str = ', '.join(['"%s"' % t for t in self.term])
        else:
            terms_str = ''
        return '%s(%s)' % (self.__class__.__name__, terms_str)

    def __repr__(self):
        return str(self)


class ExperimentalFormVocabulary(ControlledVocabulary):
    """BioPAX ExperimentalFormVocabulary."""
    pass


class RelationshipTypeVocabulary(ControlledVocabulary):
    """BioPAX RelationshipTypeVocabulary."""
    pass


class CellularLocationVocabulary(ControlledVocabulary):
    """BioPAX CellularLocationVocabulary."""
    pass


class EntityReferenceTypeVocabulary(ControlledVocabulary):
    """BioPAX EntityReferenceTypeVocabulary."""
    pass


class PhenotypeVocabulary(ControlledVocabulary):
    """BioPAX PhenotypeVocabulary."""
    pass


class TissueVocabulary(ControlledVocabulary):
    """BioPAX TissueVocabulary."""
    pass


class EvidenceCodeVocabulary(ControlledVocabulary):
    """BioPAX EvidenceCodeVocabulary."""
    pass


class SequenceModificationVocabulary(ControlledVocabulary):
    """BioPAX SequenceModificationVocabulary."""
    pass


class SequenceRegionVocabulary(ControlledVocabulary):
    """BioPAX SequenceRegionVocabulary."""
    pass


class InteractionVocabulary(ControlledVocabulary):
    """BioPAX InteractionVocabulary."""
    pass


class CellVocabulary(ControlledVocabulary):
    """BioPAX CellVocabulary."""
    pass
