import os
import re
import pybiopax
from pybiopax.biopax import *

here = os.path.dirname(os.path.abspath(__file__))


def test_process_owl():
    test_file = os.path.join(here, 'biopax_test.owl.gz')
    model = pybiopax.model_from_owl_gz(test_file)
    assert len(model.objects) == 58027, len(model.objects)
    assert 'BiochemicalReaction_a75d6aaebf5be718d981d95355ced14a' in \
        model.objects
    bcr = model.objects['BiochemicalReaction_a75d6aaebf5be718d981d95355ced14a']
    assert bcr.display_name == \
        'STATE_TRANSITION_LEFT__Raf-RIGHT__Raf-_r21'
    assert isinstance(bcr.left, list)
    assert isinstance(bcr.left[0], Protein)
    assert isinstance(bcr.right, list)
    assert isinstance(bcr.right[0], Protein)

    pub = model.objects['PublicationXref_http___www_phosphosite_org_'
                        'phosphosite_owl_recid_11958410']
    assert len(pub.comment) == 1
    assert pub.comment[0].startswith('REPLACED')
    assert pub.url[0].startswith('http://www.phosphosite')
    assert pub.year == '2010', pub.year


def test_process_molecular_interactions():
    test_file = os.path.join(here, 'molecular_interactions_test.owl')
    model = pybiopax.model_from_owl_file(test_file)
    assert len(model.objects) == 62
    mol_int = \
        model.objects['MolecularInteraction_1e82d9951c7d71c02ee6e7bdc7cb8e47']
    assert isinstance(mol_int.participant, list)
    assert len(mol_int.participant) == 2
    disp_names = {part.display_name for part in mol_int.participant}
    assert disp_names == {'ALG6', 'ALG8'}
    names = set.union(*[set(part.name) for part in mol_int.participant])
    assert names == {'ALG8', 'CDG1H', 'CDG1C', 'ALG6, CDG1C', 'ALG6',
                     'ALG8, CDG1H, MGC2840'}, names

    # Smoke test serialization
    pybiopax.model_to_owl_file(model, 'test_output.owl')
    model = pybiopax.model_from_owl_file('test_output.owl')
    assert len(model.objects) == 62

    # Test serialization into string
    owl_str = pybiopax.model_to_owl_str(model)
    model = pybiopax.model_from_owl_str(owl_str)
    assert len(model.objects) == 62


def test_get_netpath():
    m = pybiopax.model_from_netpath("22")
    assert isinstance(m, BioPaxModel)
    assert 0 < len(m.objects)


def test_get_reactome():
    m = pybiopax.model_from_reactome("177929")
    assert isinstance(m, BioPaxModel)
    assert re.match("http://www.reactome.org/biopax/\d+/177929#", m.xml_base)
    assert 0 < len(m.objects)


def test_get_humancyc():
    m = pybiopax.model_from_humancyc("PWY66-398")
    assert isinstance(m, BioPaxModel)
    assert m.xml_base is not None
    assert 0 < len(m.objects)


def test_get_biocyc():
    m = pybiopax.model_from_biocyc("P105-PWY")
    assert isinstance(m, BioPaxModel)
    assert m.xml_base is not None
    # This is garbage:
    # 'http://http://BioCyc.org//META/pathway-biopax?type=3%38object=P105-PWY'
    assert 0 < len(m.objects)


def test_get_metacyc():
    m = pybiopax.model_from_metacyc("TCA")
    assert isinstance(m, BioPaxModel)
    assert m.xml_base is not None
    assert 0 < len(m.objects)


def test_get_ecocyc():
    m = pybiopax.model_from_ecocyc("TCA")
    assert isinstance(m, BioPaxModel)
    assert m.xml_base is not None
    assert 0 < len(m.objects)
