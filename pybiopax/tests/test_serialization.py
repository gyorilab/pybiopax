from pybiopax import model_to_owl_str
from pybiopax.biopax import SequenceSite
from pybiopax.biopax.model import BioPaxModel


def test_serialize_sequence_site():
    seq_site = SequenceSite(uid='site1', sequence_position='185',
                            position_status='EQUAL')
    model = BioPaxModel(objects=[seq_site])
    model_owl = model_to_owl_str(model)
    tree = seq_site.to_xml()
    assert len(tree) == 2
    assert '185' in model_owl, seq_site.to_xml()
