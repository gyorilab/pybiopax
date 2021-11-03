# -*- coding: utf-8 -*-

import pickle
from collections import defaultdict
from typing import Optional, Type

import bioversions
import numpy as np
import pandas as pd
import seaborn
from scipy.stats import fisher_exact
from statsmodels.stats.multitest import multipletests
from tqdm import tqdm

import bioregistry
import protmapper.uniprot_client
import pybiopax
import pyobo
import pystow
from indra.sources import creeds
from indra.statements import (
    Agent,
    RegulateAmount,
    Statement,
    stmts_to_json_file,
)
from pybiopax.biopax import Protein

REACTOME_MODULE = pystow.module("bio", "reactome", bioversions.get_version("reactome"))
CREEDS_MODULE = pystow.module("bio", "creeds")


def get_reactome_human_ids() -> set[str]:
    identifiers = pyobo.get_ids("reactome")
    species = pyobo.get_id_species_mapping("reactome")
    rv = {reactome_id for reactome_id in identifiers if species[reactome_id] == "9606"}
    return rv


def get_protein_hgnc(protein: Protein) -> Optional[str]:
    if protein.entity_reference is None:
        return None
    rv = {bioregistry.normalize_prefix(xref.db): xref.id for xref in protein.entity_reference.xref}
    hgnc_id = rv.get("hgnc")
    if hgnc_id is not None:
        return hgnc_id
    uniprot_id = rv.get("uniprot")
    if uniprot_id is not None:
        hgnc_id = protmapper.uniprot_client.get_hgnc_id(uniprot_id)
        if hgnc_id:
            return hgnc_id
    uniprot_isoform_id = rv.get("uniprot.isoform")
    if uniprot_isoform_id is not None:
        hgnc_id = protmapper.uniprot_client.get_hgnc_id(uniprot_isoform_id)
        if hgnc_id:
            return hgnc_id
    return None


def ensure_reactome(reactome_id: str, force: bool = False):
    path = REACTOME_MODULE.join(name=f"{reactome_id}.xml")
    if path.is_file() and not force:
        return pybiopax.model_from_owl_file(
            path, tqdm_kwargs=dict(leave=False, desc=f"Parsing {reactome_id} OWL")
        )
    model = pybiopax.model_from_reactome(
        reactome_id, tqdm_kwargs=dict(leave=False, desc=f"Getting {reactome_id}")
    )
    pybiopax.model_to_owl_file(
        model, path, tqdm_kwargs=dict(leave=False, desc=f"Serializing {reactome_id} OWL")
    )
    return model


def get_reactome_genes(reactome_id: str) -> set[str]:
    model = ensure_reactome(reactome_id)
    rv = set()
    for protein in model.objects.values():
        if not isinstance(protein, Protein):
            continue
        if (hgnc_id := get_protein_hgnc(protein)) is not None:
            rv.add(hgnc_id)
    return rv


def get_creeds_statements(entity_type: str) -> list[Statement]:
    path = CREEDS_MODULE.join(name=f"{entity_type}_stmts.pkl")
    if path.is_file():
        with path.open("rb") as file:
            return pickle.load(file)
    url = creeds.api.urls[entity_type]
    raw_path = CREEDS_MODULE.ensure(url=url)
    processor = creeds.process_from_file(raw_path, entity_type)
    stmts_to_json_file(processor.statements, path)
    with path.open("wb") as file:
        pickle.dump(processor.statements, file, protocol=pickle.HIGHEST_PROTOCOL)
    return processor.statements


def get_hgnc_id(agent: Agent) -> Optional[str]:
    hgnc_id = agent.db_refs.get("HGNC")
    if hgnc_id is not None:
        return hgnc_id
    up_id = agent.db_refs.get("UP")
    if up_id is None:
        return None
    return protmapper.uniprot_client.get_hgnc_id(up_id)


def get_regulates(
    stmts: list[Statement],
    stmt_cls: Type[RegulateAmount] = RegulateAmount,
) -> dict[str, set[str]]:
    rv = defaultdict(set)
    for stmt in stmts:
        if not isinstance(stmt, stmt_cls):
            continue
        subj_hgnc_id = get_hgnc_id(stmt.subj)
        obj_hgnc_id = get_hgnc_id(stmt.obj)
        if subj_hgnc_id is None or obj_hgnc_id is None:
            continue
        rv[subj_hgnc_id].add(obj_hgnc_id)
    return dict(rv)


def _prepare_hypergeometric_test(
    query_gene_set: set[str],
    pathway_gene_set: set[str],
    gene_universe: int,
) -> np.ndarray:
    """Prepare the matrix for hypergeometric test calculations.

    :param query_gene_set: gene set to test against pathway
    :param pathway_gene_set: pathway gene set
    :param gene_universe: number of HGNC symbols
    :return: 2x2 matrix
    """
    return np.array(
        [
            [
                len(query_gene_set.intersection(pathway_gene_set)),
                len(query_gene_set.difference(pathway_gene_set)),
            ],
            [
                len(pathway_gene_set.difference(query_gene_set)),
                gene_universe - len(pathway_gene_set.union(query_gene_set)),
            ],
        ]
    )


def _main():
    reactome_ids = get_reactome_human_ids()
    reactome_it = [
        (reactome_id, get_reactome_genes(reactome_id))
        for reactome_id in tqdm(reactome_ids, desc="Downloading Reactome pathways")
    ]

    universe_size = len(pyobo.get_ids("hgnc"))
    creeds_drug_stmts = get_creeds_statements("gene")
    creeds_drug_hgncs = get_regulates(creeds_drug_stmts)

    dfs = []
    for pert_id, pert_genes in tqdm(creeds_drug_hgncs.items()):
        rows = []
        for reactome_id, reactome_genes in tqdm(reactome_it, leave=False):
            table = _prepare_hypergeometric_test(pert_genes, reactome_genes, universe_size)
            _, p_value = fisher_exact(table, alternative="greater")
            rows.append((f"hgnc:{pert_id}", f"reactome:{reactome_id}", p_value))
        df = pd.DataFrame(rows, columns=["perturbation", "pathway", "p"])
        correction_test = multipletests(df["p"], method="fdr_bh")
        df["q"] = correction_test[1]
        df["mlq"] = -np.log10(df["q"])  # minus log q
        df.sort_values("q", inplace=True)
        dfs.append(df)

    path = CREEDS_MODULE.join(name="analysis.tsv")
    full_df = pd.concat(dfs)
    full_df.to_csv(path, sep="\t", index=False)
    print("output to", path)

    df_square = full_df.pivot(index="pathway", columns="perturbation")["mlq"]
    img_path = CREEDS_MODULE.join(name="analysis.tsv")
    g = seaborn.clustermap(df_square)
    g.savefig(img_path)


if __name__ == "__main__":
    _main()
