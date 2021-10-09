from pybiopax.biopax import *
from pybiopax.paths import find_objects, BiopaxClassConstraintError


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


def test_find_objects_constraints():
    xr1 = UnificationXref(uid='2')
    xr2 = PublicationXref(uid='3')
    xr3 = RelationshipXref(uid='4')
    protref = EntityReference(uid='1', xref=[xr1, xr2, xr3])
    xr1._xref_of = [protref]
    xr2._xref_of = [protref]
    xr3._xref_of = [protref]

    objects = find_objects(protref, 'xref')
    assert len(objects) == 3

    objects = find_objects(protref, 'xref:Xref')
    assert len(objects) == 3

    objects = find_objects(protref, 'xref:UnificationXref')
    assert len(objects) == 1
    assert objects[0] == xr1

    objects = find_objects(protref, 'xref:UnificationXref/xref_of')
    assert len(objects) == 1
    assert objects[0] == protref, objects
