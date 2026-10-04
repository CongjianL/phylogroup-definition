# Output contract

## Required analysis products

Use a project-appropriate directory, but keep these logical products.

### Membership and definitions

`PHYLOGROUP_MEMBERSHIP.tsv`

One row per ingroup genome. Recommended columns:

- `GenomeID`
- `phylogroup`
- `status` (`RESOLVED` or `UNRESOLVED_PHYLOGROUP`)
- `tree_node_id`
- `tree_monophyletic`
- `branch_support`
- `tree_stability`
- `AAI_stability`
- `ANI_AF_stability`
- `consensus_stability`
- optional display-only taxonomy/metadata columns

`PHYLOGROUP_DEFINITIONS.tsv`

One row per PG. Include:

- deterministic PG ID;
- member count;
- exact tree node;
- branch support;
- parameter-stability summaries;
- within and nearest-between patristic summaries;
- within and nearest-between AAI plus coverage;
- ANI/AF structure summary;
- cross-view agreement status;
- unresolved limitations.

### Per-view results

Retain:

- all parameter-sweep partitions;
- co-assignment matrix per view;
- chosen/stable representative partition per view;
- network edge tables with exact weights/parameters;
- stochastic seed records when applicable.

### Cross-view results

Produce:

- ARI/NMI/VI table;
- consensus or fused similarity matrix;
- consensus/fusion partition;
- monophyly reconciliation table;
- conflict/unresolved ledger.

### Validation summaries

For each final PG report descriptive within/between distributions for:

- patristic distance;
- AAI;
- AAI/protein coverage;
- ANI;
- AF.

If POCP exists, summarize it **after** final PG freezing as an auxiliary validation metric.

## Recommended figures

1. Canonical rooted tree with deterministic PG ring/bar and optional current taxonomy/habitat annotations.
2. Tree-view co-assignment/stability heatmap.
3. AAI co-assignment/stability heatmap.
4. ANI/AF co-assignment/stability heatmap.
5. Cross-view partition-concordance heatmap (ARI/NMI/VI or equivalent).
6. Consensus/fused network with PG membership.
7. Final tree-aligned relatedness heatmaps.
8. Within-vs-nearest-between distribution figure for each major PG.

Use the canonical tree tip order for tree-aligned heatmaps unless there is a documented reason not to.

## Report structure

`PHYLOGROUP_DEFINITION_REPORT.md`

Recommended sections:

1. Objective and frozen inputs
2. Cohort and input validation
3. Phylogenetic clustering
4. AAI clustering
5. ANI/AF clustering
6. Parameter stability
7. Cross-view concordance
8. Consensus/fusion result
9. Monophyly enforcement
10. Final operational phylogroups
11. Unresolved genomes/boundaries
12. Optional POCP/posthoc validation
13. Limitations
14. Provenance and reproducibility
15. Human review stop

The report must distinguish calculated evidence from interpretation and must not claim formal taxonomic revision.
