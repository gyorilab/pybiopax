import pytest
from pybiopax.biopax import *
from pybiopax import model_from_pc_query
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

    objects = find_objects(protref, 'xref:UnificationXref/xref_of:RnaReference')
    assert not objects


def test__with_invalid_class():
    xr1 = UnificationXref(uid='1')

    with pytest.raises(BiopaxClassConstraintError):
        find_objects(xr1, 'xref_of:XXX')


def test_recursive():
    p1 = Protein(uid='1')
    c1 = Complex(uid='2', member_physical_entity=[p1])
    c2 = Complex(uid='3', member_physical_entity=[c1])

    objects = find_objects(c2, 'member_physical_entity')
    assert len(objects) == 1
    assert objects[0] == c1

    objects = find_objects(c2, 'member_physical_entity/member_physical_entity')
    assert len(objects) == 1
    assert objects[0] == p1

    objects = find_objects(c2, 'member_physical_entity*')
    assert len(objects) == 2, objects
    assert set(objects) == {p1, c1}


def test_multi_step():
    model = model_from_pc_query('pathsfromto', ['MAP2K1'], ['MAPK1'])
    bcr = model.objects['BiochemicalReaction_4f689747397d98089c551022a3ae2d88']
    assert len(find_objects(bcr, 'left')) == 1
    assert len(find_objects(bcr, 'left/entity_reference')) == 1
    objs = find_objects(bcr, 'left/entity_reference/entity_reference_of')
    assert len(objs) == 10
