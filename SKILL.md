---
name: phylogroup-definition
description: Define reusable, operational microbial phylogroups from genome-scale evolutionary evidence. Use when analyzing bacterial or archaeal genome collections to replace unstable genus labels with phylogenetically coherent groups, or when asked for multi-view clustering using a canonical species tree/patristic distances, AAI, and ANI with aligned fraction (AF). The workflow emphasizes monophyly, parameter-sweep stability, network/community analysis, and cross-view consensus. It explicitly keeps orthogroup/gene-content data out of the primary definition so they can remain an independent downstream validation layer. It is not a formal taxonomic naming or genus-revision workflow.
---

# Phylogroup Definition

## Core principle

Define phylogroups as **operational evolutionary units**, not formal taxonomic ranks.

Use three primary views:

1. canonical phylogeny / patristic distance;
2. AAI with comparison coverage;
3. ANI together with aligned fraction (AF).

Treat phylogeny as the backbone, AAI as deep genome-wide support, and ANI/AF as a shallower neighborhood view. Keep orthogroup, pangenome, function, habitat, phenotype, and taxonomy labels out of primary clustering unless the user explicitly requests a different design.

Read `references/methodology.md` before designing or interpreting the analysis. Read `references/output-contract.md` before producing the final deliverables.

## Workflow

### 1. Freeze inputs and scope

Identify and record:

- one canonical rooted species tree with branch lengths;
- branch-support representation and the project's accepted support convention, if any;
- the ingroup genome/tip set;
- AAI matrix or complete pairwise table, plus protein/alignment coverage when available;
- ANI matrix or pairwise table **and AF**;
- optional POCP matrix for post-definition validation only;
- optional metadata for display/interpretation only.

Do not silently change the cohort, reroot/rebuild the tree, recalculate similarity matrices, or add reference genomes when validated inputs already exist. If a required input is absent, state the gap before substituting another metric.

Run `scripts/validate_matrices.py` when wide pairwise matrices are supplied. Use it to verify label identity, symmetry, missingness, and observed ranges before clustering.

### 2. Build the phylogenetic view

Use the canonical tree directly.

Preferred analysis:

- run at least one tree-native clustering method such as TreeCluster or PhyCLIP when feasible;
- derive a patristic-distance similarity or mutual-kNN graph and run a community method such as Leiden;
- sweep reasonable distance/network/resolution parameters rather than choosing one visually convenient setting;
- preserve existing branch support and topology.

A final phylogroup must map to a monophyletic subtree. A network community that is non-monophyletic is not acceptable unchanged: split it along supported tree structure or mark the boundary unresolved.

Use `scripts/check_monophyly.py` for deterministic membership checks against the rooted tree.

### 3. Build the AAI view

Use AAI as an independent deep genomic-similarity view.

- Do not impose a universal genus-like AAI cutoff.
- Keep identity and coverage separate.
- Construct a distance/similarity representation from AAI.
- Prefer locally scaled or mutual-kNN graphs over arbitrary hard edges when no biological discontinuity is established.
- Sweep neighborhood and community-resolution parameters.
- Record co-assignment frequencies across the sweep.

If AAI values are based on low or heterogeneous protein coverage, retain that limitation in the evidence table instead of filtering it away silently.

### 4. Build the ANI/AF view

Treat ANI and AF jointly.

- Do not use ANI alone as a family-scale distance.
- Do not force a 95% ANI species threshold to define deeper phylogroups.
- Distinguish high-ANI/high-AF relationships from high-ANI/low-AF relationships.
- Explore graph/community structure across reasonable ANI/AF transformations or edge rules.
- Interpret stable ANI/AF clusters primarily as shallow structure unless they coincide with deeper tree/AAI boundaries.

Document the exact ANI/AF edge function or kernel. Never hide low AF behind a single ANI number.

### 5. Measure stability within each view

For each parameter sweep:

- retain every partition and parameter set;
- create a genome-by-genome co-assignment matrix;
- identify stable plateaus rather than a single optimum chosen by appearance;
- record unresolved or unstable genomes/boundaries.

Use `scripts/coassignment.py` to build a deterministic co-assignment matrix from a table of sweep partitions.

### 6. Compare views

Compare the tree, AI, and ANI/AF partitions with at least:

- Adjusted Rand Index (ARI);
- Normalized Mutual Information (NMI);
- Variation of Information (VI).

Use `scripts/partition_metrics.py` when partitions are tabulated by genome.

Interpret agreement asymmetrically:

- tree + AAI convergence is strong evidence for a deeper phylogroup boundary;
- ANI/AF splitting inside a tree+AAI group usually indicates shallower substructure;
- ANI/AF disagreement that spans strong monophyletic tree+AAI groups is a conflict to inspect, not an automatic override.

### 7. Integrate the evolutionary views

Use a transparent consensus approach. Acceptable options include:

- consensus of per-view co-assignment matrices;
- Similarity Network Fusion (SNF) across normalized tree, AAI, and ANI/AF similarities;
- another documented multi-view fusion method.

Always retain a simpler consensus/co-assignment result as a sensitivity analysis if using SNF or another complex fusion method.

Do **not** let a fused network override monophyly. Map all fused communities back onto the canonical tree and enforce the tree constraint.

### 8. Freeze operational phylogroups

Assign a phylogroup only when the evidence supports a stable operational unit.

Default decision logic:

1. require monophyly on the canonical tree;
2. require adequate branch support according to the project-defined convention, or explicitly mark support as weak/uncertain;
3. require stability across a reasonable phylogenetic clustering parameter range;
4. seek independent reinforcement from AAI structure;
5. use ANI/AF to characterize or refine shallow structure, not to overrule a coherent deeper group without explicit evidence;
6. allow `UNRESOLVED_PHYLOGROUP` rather than forcing every genome into a stable group.

Assign neutral deterministic identifiers such as `PG01`, `PG02`, ... in rooted-tree traversal order. Do not use genus names as phylogroup identifiers.

### 9. Post-definition validation only

After phylogroups are frozen, optional independent validation may include:

- POCP within vs between phylogroups;
- orthogroup/gene-content clustering;
- pangenome structure;
- functional profiles;
- habitat/phenotype associations;
- current taxonomy/GTDB labels.

Do not use orthogroup/gene-content evidence to retroactively tune the primary phylogroup boundaries if those same data will be analyzed downstream as outcomes. This prevents circularity.

### 10. Deliver and stop for review

Generate the outputs in `references/output-contract.md` and stop at a human review gate before replacing genus or another grouping variable in downstream analyses.

Do not claim formal taxonomic revision, new genera, new combinations, or nomenclatural acts from this workflow.

## Quality gates

Before calling the analysis complete, verify all of the following:

- identical ingroup labels across required inputs or an explicit reconciliation table;
- no non-monophyletic final phylogroup;
- no hidden universal AAI/ANI/AF cutoff presented as taxonomic law;
- ANI interpreted together with AF;
- parameter sweeps and stability/co-assignment retained;
- tree, AAI, and ANI/AF agreement quantified;
- final PG identifiers deterministic;
- unresolved cases preserved rather than force-assigned;
- taxonomy and gene content used only as annotations/validation unless explicitly authorized otherwise;
- exact software versions, parameters, random seeds, input hashes, and output hashes recorded.

## Common user requests this skill should handle

- "Define phylogroups for these bacterial genomes from my tree, AAI and ANI matrices."
- "Replace genus with phylogenetically coherent groups for downstream comparative genomics."
- "Build a multi-view tree + AAI + ANI/AF consensus clustering workflow."
- "Check whether my proposed phylogroups are stable and monophyletic."
- "Compare tree, AAI and ANI partitions and freeze neutral PG labels."
