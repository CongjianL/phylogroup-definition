# Phylogroup Definition

A reusable workflow and ChatGPT Skill for defining **operational microbial phylogroups** from genome-scale evolutionary evidence.

The framework is designed for bacterial or archaeal comparative genomics projects where formal genus assignments are unstable, non-monophyletic, incomplete, or simply not the most useful unit for downstream evolutionary analysis.

Instead of treating taxonomy as the clustering target, this workflow defines phylogroups from three complementary evolutionary views:

1. **Canonical phylogeny / patristic distance**
2. **Average Amino Acid Identity (AAI)**
3. **Average Nucleotide Identity (ANI) together with aligned fraction (AF)**

Orthogroup composition, pangenome structure, functional profiles, habitat, phenotype, and taxonomic labels are intentionally kept **outside the primary phylogroup definition** so they can be used later as independent validation or downstream response variables.

---

## Scientific principle

The central idea is:

> **Phylogeny defines the evolutionary backbone; AAI provides deeper genome-wide support; ANI/AF resolves shallower genomic structure; gene content and ecology validate the resulting phylogroups independently.**

A final phylogroup should therefore be:

- monophyletic on a frozen canonical species tree;
- stable across reasonable phylogenetic clustering parameters;
- independently supported by AAI structure;
- consistent with, or at least explicitly interpretable against, ANI/AF structure;
- assigned a neutral identifier such as `PG01`, `PG02`, etc.;
- treated as an operational evolutionary unit rather than a formal taxonomic rank.

The workflow explicitly allows `UNRESOLVED_PHYLOGROUP` when a boundary is unstable or conflicting.

---

## Why not define phylogroups from orthogroups?

If gene-content differences will later be analyzed as a biological outcome, using orthogroup composition to define the same groups creates circularity.

The recommended design is:

```text
species tree + patristic distance
              +
             AAI
              +
           ANI / AF
              |
              v
     consensus phylogroups
              |
              v
 orthogroup / pangenome validation
              |
              v
 function / habitat / adaptation
```

This keeps downstream findings such as “phylogroups explain gene-content structure” scientifically independent of the group-definition procedure.

---

## Workflow overview

### 1. Freeze the input dataset

Use one immutable genome cohort and one canonical rooted species tree.

Required inputs normally include:

- rooted species tree with branch lengths;
- tip/genome identifier mapping;
- branch support values;
- pairwise AAI matrix or table;
- AAI protein/alignment coverage when available;
- pairwise ANI matrix or table;
- ANI aligned fraction (AF).

Optional post-definition inputs include POCP, taxonomy, habitat, phenotype, and gene-content data.

---

### 2. Phylogenetic view

Use the canonical tree as the primary structural constraint.

Recommended analyses include:

- tree-native clustering with TreeCluster, PhyCLIP, or an equivalent method;
- patristic-distance similarity or mutual-kNN networks;
- Leiden or Infomap community detection as sensitivity analyses;
- parameter sweeps rather than a single visually chosen threshold.

A final phylogroup must correspond to a **monophyletic subtree**.

Network communities that are non-monophyletic must be split using the tree or retained as unresolved.

---

### 3. AAI view

AAI is treated as an independent deep genomic-similarity layer.

Recommended strategy:

- convert AAI to an explicit similarity/distance representation;
- retain identity and comparison coverage separately;
- construct locally scaled or mutual-kNN networks;
- sweep neighborhood and community-resolution parameters;
- summarize stability using genome-pair co-assignment frequencies.

The workflow does **not** assume a universal AAI cutoff for genus or phylogroup boundaries.

---

### 4. ANI/AF view

ANI must be interpreted together with aligned fraction.

A high ANI based on limited genomic overlap is not treated as equivalent to a high-ANI/high-AF comparison.

ANI/AF is primarily used to:

- detect shallow genomic neighborhoods;
- identify species-like structure nested inside deeper phylogroups;
- flag conflicts with tree/AAI-defined boundaries.

The workflow does **not** use a fixed 95% ANI threshold to define family-scale phylogroups.

---

### 5. Parameter stability

Each clustering view should be explored across a bounded, documented parameter grid.

For every view:

- retain all tested partitions;
- build a genome-by-genome co-assignment matrix;
- identify stable parameter plateaus;
- track genomes that frequently switch groups;
- avoid choosing parameters solely because the final plot looks clean.

---

### 6. Cross-view comparison

Compare tree, AAI, and ANI/AF partitions using at least:

- Adjusted Rand Index (**ARI**)
- Normalized Mutual Information (**NMI**)
- Variation of Information (**VI**)

Interpretation is intentionally asymmetric:

- tree + AAI convergence is strong support for a deeper phylogroup;
- ANI/AF splitting inside a stable tree+AAI group usually indicates shallower structure;
- ANI/AF conflicts do not automatically override a strongly supported monophyletic lineage.

---

### 7. Multi-view integration

Integrate the three evolutionary views using a transparent consensus strategy.

Supported approaches include:

- co-assignment consensus;
- Similarity Network Fusion (**SNF**);
- another explicitly documented multi-view fusion method.

A fused network is never allowed to override the monophyly requirement.

Every proposed consensus group must be mapped back to the canonical tree.

---

### 8. Freeze operational phylogroups

Use deterministic neutral labels such as:

```text
PG01
PG02
PG03
...
```

Order identifiers by rooted-tree traversal so numbering is reproducible.

For every phylogroup retain:

- exact membership;
- defining tree node;
- branch support;
- phylogenetic-clustering stability;
- AAI stability;
- ANI/AF stability;
- consensus stability;
- within-group relatedness distributions;
- nearest between-group relatedness distributions;
- unresolved limitations.

---

### 9. Independent validation

After phylogroups are frozen, optional validation can use:

- POCP;
- orthogroup presence/absence;
- pangenome structure;
- functional profiles;
- habitat;
- phenotype;
- current taxonomy or GTDB labels.

These data should normally **not** be used to retroactively tune the primary phylogroup boundaries.

---

## Repository structure

```text
phylogroup-definition/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── methodology.md
│   ├── output-contract.md
│   └── api_reference.md
└── scripts/
    ├── check_monophyly.py
    ├── coassignment.py
    ├── partition_metrics.py
    └── validate_matrices.py
```

### Core files

- **`SKILL.md`** — main reusable workflow and execution rules.
- **`references/methodology.md`** — scientific rationale and implementation guidance.
- **`references/output-contract.md`** — recommended result tables, figures, and report structure.
- **`references/api_reference.md`** — dependency and software-use notes.

### Helper scripts

- **`validate_matrices.py`** — validate matrix shape, labels, symmetry, missingness, and observed ranges.
- **`check_monophyly.py`** — verify that proposed phylogroups are exactly monophyletic.
- **`coassignment.py`** — derive co-assignment and comparable-count matrices from parameter-sweep partitions.
- **`partition_metrics.py`** — calculate ARI, NMI, and VI between clustering solutions.

---

## Minimal expected outputs

A complete analysis should normally produce:

```text
PHYLOGROUP_MEMBERSHIP.tsv
PHYLOGROUP_DEFINITIONS.tsv

per-view partitions
parameter-sweep tables
co-assignment matrices

ARI_NMI_VI comparisons
consensus/fused similarity matrix
monophyly reconciliation table
unresolved/conflict ledger

PHYLOGROUP_DEFINITION_REPORT.md
```

Recommended figures include:

- canonical rooted tree with phylogroup annotation;
- tree-view co-assignment heatmap;
- AAI co-assignment heatmap;
- ANI/AF co-assignment heatmap;
- cross-view concordance heatmap;
- consensus/fused network;
- final tree-aligned relatedness heatmaps.

See [`references/output-contract.md`](references/output-contract.md) for the complete output specification.

---

## Example requests

This Skill is intended for requests such as:

- “Define phylogroups for these bacterial genomes from my species tree, AAI, ANI and AF matrices.”
- “Replace genus with phylogenetically coherent groups for downstream comparative genomics.”
- “Build a tree + AAI + ANI/AF consensus clustering workflow.”
- “Check whether these proposed phylogroups are stable and monophyletic.”
- “Compare phylogenetic, AAI and ANI partitions and assign neutral PG labels.”

---

## Important limitations

This workflow does **not**:

- perform formal taxonomic revision;
- propose new genus names or nomenclatural combinations;
- treat current genus labels as clustering inputs;
- assume universal AAI or ANI thresholds;
- use orthogroup/gene-content information as a primary grouping criterion;
- force every genome into a resolved phylogroup.

Phylogroups are operational evolutionary units for comparative analysis, not replacements for formal bacterial or archaeal nomenclature.

---

## Reproducibility

For every analysis, record:

- exact input hashes;
- software versions;
- command lines;
- clustering parameters;
- random seeds;
- parameter grids;
- final membership hashes;
- output hashes.

The final phylogroup framework should be frozen before it is used as a grouping variable in downstream comparative genomics, pangenome, functional, ecological, or adaptation analyses.
