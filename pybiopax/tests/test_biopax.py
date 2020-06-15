import os
from pybiopax.biopax import *
from pybiopax import model_from_owl_file

here = os.path.dirname(os.path.abspath(__file__))
test_file = os.path.join(here, 'biopax_test.owl')


def test_process_owl():
    model = model_from_owl_file(test_file)
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
    assert pub.url.startswith('http://www.phosphosite')
    assert pub.year == '2010', pub.year
