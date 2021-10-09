from pybiopax.biopax import *
from pybiopax.paths import find_objects


def test_find_objects():
    protref = EntityReference(uid='1')
    prot = Protein(uid='2', standard_name='x', entity_reference=protref)
    protref._entity_reference_of = [prot]

    # Forward reference
    objects = find_objects(prot, 'entity_reference')
    assert len(objects) == 1, objects
    assert objects[0] == protref

    # Reverse reference
    objects = find_objects(protref, 'entity_reference_of')
    assert len(objects) == 1, objects
    assert objects[0] == prot, objects

    # Multi-step
    objects = find_objects(prot, 'entity_reference/entity_reference_of')
    assert len(objects) == 1, objects
    assert objects[0] == prot, objects
