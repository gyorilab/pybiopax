# -*- coding: utf-8 -*-

"""Tests for :mod:`pybiopax.tools`."""

import unittest

from pybiopax.biopax import (
    BiochemicalReaction,
    ControlledVocabulary,
    FragmentFeature,
    ModificationFeature,
    Protein,
    ProteinReference,
    RelationshipXref,
    SmallMolecule,
    UnificationXref,
)
from pybiopax.tools import (
    get_simple_physical_entity_xrefs,
    is_modification_reaction,
    iter_modifications,
)


class TestTools(unittest.TestCase):
    """A test case for PyBioPAX model traversal tools."""

    def test_get_xrefs(self):
        """Test getting Xrefs."""
        protein = Protein(
            uid="...",
            display_name="YFG",
            entity_reference=ProteinReference(
                uid="...",
                xref=[
                    UnificationXref(uid="...", db="db", id="id"),
                    # Add this since in PC there are a lot of duplicates like this
                    RelationshipXref(uid="...", db="db", id="id", relationship_type="identity"),
                ],
            ),
        )
        self.assertEqual({("db", "id")}, get_simple_physical_entity_xrefs(protein))

    def test_not_modification_reaction(self):
        """Test the predicate for modification reactions."""
        false_examples = [
            (None, "Wrong type"),
            (
                BiochemicalReaction(
                    uid="...",
                    left=[..., ...],
                    right=[...],
                ),
                "Non-singular reactant",
            ),
            (
                BiochemicalReaction(
                    uid="...",
                    left=[...],
                    right=[..., ...],
                ),
                "Non-singular product",
            ),
            (
                BiochemicalReaction(
                    uid="...",
                    left=[SmallMolecule(uid=...)],
                    right=[Protein(uid="...")],
                ),
                "Non-protein reactant",
            ),
            (
                BiochemicalReaction(
                    uid="...",
                    left=[Protein(uid="...")],
                    right=[SmallMolecule(uid="...")],
                ),
                "Non-protein product",
            ),
            (
                BiochemicalReaction(
                    uid="...",
                    left=[
                        Protein(
                            uid="...",
                            entity_reference=ProteinReference(
                                uid="...",
                                xref=[
                                    UnificationXref(uid="...", db="db", id="id1"),
                                ],
                            ),
                        )
                    ],
                    right=[
                        Protein(
                            uid="...",
                            entity_reference=ProteinReference(
                                uid="...",
                                xref=[
                                    UnificationXref(uid="...", db="db", id="id2"),
                                ],
                            ),
                        )
                    ],
                ),
                "Mismatch IDs",
            ),
        ]
        for test, reason in false_examples:
            with self.subTest(reason=reason):
                self.assertFalse(is_modification_reaction(test), msg=reason)

    def test_is_modification_reaction(self):
        """Test the predicate for modification reactions."""
        self.assertTrue(
            is_modification_reaction(
                BiochemicalReaction(
                    uid="...",
                    left=[
                        Protein(
                            uid="...",
                            entity_reference=ProteinReference(
                                uid="...",
                                xref=[
                                    UnificationXref(uid="...", db="db", id="id"),
                                ],
                            ),
                        )
                    ],
                    right=[
                        Protein(
                            uid="...",
                            entity_reference=ProteinReference(
                                uid="...",
                                xref=[
                                    UnificationXref(uid="...", db="db", id="id"),
                                ],
                            ),
                        )
                    ],
                ),
            )
        )

    def test_modifications(self):
        """Test searching for modifications."""
        protein = Protein(
            uid="...",
            display_name="YFG",
        )
        self.assertEqual([], list(iter_modifications(protein, "phospho")))

        protein = Protein(
            uid="...",
            display_name="YFG",
            features=[
                FragmentFeature(uid="..."),
            ],
        )
        self.assertEqual([], list(iter_modifications(protein, "phospho")))

        protein = Protein(
            uid="...",
            display_name="YFG",
            features=[
                ModificationFeature(uid="..."),
            ],
        )
        self.assertEqual([], list(iter_modifications(protein, "phospho")))

        protein = Protein(
            uid="...",
            display_name="YFG",
            features=[
                ModificationFeature(uid="...", modification_type=ControlledVocabulary(["nope"])),
            ],
        )
        self.assertEqual([], list(iter_modifications(protein, "phospho")))

        protein = Protein(
            uid="...",
            display_name="YFG",
            features=[
                ModificationFeature(modification_type=ControlledVocabulary(["phospho"])),
            ],
        )
        self.assertEqual(
            [ModificationFeature(modification_type=ControlledVocabulary(["phospho"]))],
            list(iter_modifications(protein, "phospho")),
        )
