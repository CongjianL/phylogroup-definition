# Methodology reference

## Contents

1. Scientific model
2. Evidence hierarchy
3. Network construction
4. Parameter sweeps and consensus
5. Monophyly constraint
6. Interpretation of AAI and ANI/AF
7. Circularity guardrail
8. Optional software choices
9. Failure modes

## 1. Scientific model

The goal is to identify operational phylogroups: reproducible evolutionary units that are useful for comparative genomics without claiming formal taxonomic rank.

A useful conceptual hierarchy is:

- **phylogeny**: vertical evolutionary backbone;
- **AAI**: deeper genome-wide protein similarity;
- **ANI/AF**: shallower nucleotide-level neighborhood structure;
- **gene content/function/ecology**: downstream validation and biological interpretation.

The method is intentionally multi-view because no single distance metric should be assumed to define all bacterial or archaeal ranks.

## 2. Evidence hierarchy

### Primary backbone: canonical phylogeny

Require final phylogroups to be monophyletic on one explicitly frozen tree. Preserve branch lengths and native support values. Tree-native clustering is preferred because ordinary graph communities do not know what monophyly means.

### Primary independent support: AAI

Use AAI to test whether tree-defined lineages also have genome-wide protein-level coherence. Keep alignment/protein coverage as a separate field. Avoid a fixed genus threshold unless a study-specific discontinuity is independently demonstrated and sensitivity-tested.

### Secondary/shallow support: ANI + AF

ANI is most informative for closer genomes. At deeper scales, ANI values can be based on limited aligned sequence. Always retain AF and distinguish high-coverage from low-coverage comparisons.

### Independent downstream validation

POCP, orthogroup repertoire, pangenome structure, function, habitat and phenotype can be highly informative, but should normally be used after primary phylogroups are frozen when those same data will be tested as downstream responses.

## 3. Network construction

Do not require a single universal graph recipe. Choose one or more of these and document the transformation exactly.

### Patristic network

Input: pairwise patristic distance `d_ij`.

Possible similarities:

- Gaussian/local kernel: `s_ij = exp(-d_ij^2 / (sigma_i sigma_j))`;
- mutual-kNN graph using smallest patristic distances;
- threshold graph only when a defensible distance discontinuity exists.

### AAI network

Input: AAI identity and coverage.

Possible similarities:

- normalized AAI similarity with low-coverage relationships retained as metadata;
- mutual-kNN on `1 - AAI`;
- locally scaled kernel.

Do not multiply by coverage without explaining the biological meaning; identity and coverage should remain auditable even if a composite kernel is used.

### ANI/AF network

Input: ANI and AF.

Use a joint rule or kernel. Examples include:

- require a minimum AF before an ANI edge is eligible;
- define a composite similarity that monotonically increases with both ANI and AF;
- use a multilayer graph with ANI and AF as separate edge attributes.

Treat the chosen transformation as an analysis choice and sweep it when reasonable.

## 4. Parameter sweeps and consensus

Community algorithms such as Leiden have resolution and neighborhood parameters. Do not select a single value because the picture looks clean.

For each view:

1. define a bounded scientifically reasonable parameter grid;
2. run multiple seeds when the algorithm is stochastic;
3. record every partition;
4. compute pairwise co-assignment frequency;
5. identify plateaus where memberships are stable;
6. report genomes that frequently switch communities.

A co-assignment value near 1 means two genomes repeatedly cluster together across the tested settings. A value near 0.5 indicates an unstable boundary, not half-membership in a biological sense.

## 5. Monophyly constraint

Every final phylogroup must correspond to a connected subtree containing exactly its members.

If a network community is non-monophyletic:

- inspect whether it is the union of two or more strongly supported clades;
- split by tree structure when this preserves coherent evidence;
- otherwise mark the case unresolved.

Do not use a well-supported enclosing MRCA as support for a non-monophyletic subset.

## 6. Interpretation of AAI and ANI/AF

### AAI

Prefer distributions over single averages. Report at least:

- within-group median and range/IQR;
- group-to-sister median and range/IQR;
- protein/alignment coverage;
- overlap or observed gaps.

A clean observed gap is useful descriptive evidence, not a universal rank threshold.

### ANI/AF

Use ANI/AF to identify species-like or shallow genomic neighborhoods and to detect internal substructure. If ANI clusters are nested within a stable tree+AAI phylogroup, retain the deeper phylogroup and optionally describe subphylogroups/species clusters separately.

## 7. Circularity guardrail

If orthogroup/gene-content structure will later be analyzed as an outcome, do not let it define the primary phylogroups. Otherwise a later result such as "phylogroups explain gene-content variation" becomes partly tautological.

A strong design is:

`tree + AAI + ANI/AF -> phylogroups -> independent orthogroup/pangenome validation -> ecological/functional analysis`

## 8. Optional software choices

Use what is available and version-pin it. Suitable tools include:

- tree clustering: TreeCluster, PhyCLIP, or a documented equivalent;
- tree parsing/distances: Biopython, ETE, DendroPy;
- graph construction: igraph, NetworkX;
- communities: Leiden, Infomap;
- multi-view fusion: SNF or a documented consensus matrix;
- partition comparison: ARI, NMI, VI.

Do not make availability of one named package a scientific requirement. If a tool is unavailable, use an equivalent method and document the substitution.

## 9. Failure modes

Avoid these patterns:

- genus labels used as clustering features;
- one arbitrary AAI/ANI cutoff defining every group;
- ANI reported without AF at deep divergence;
- Leiden communities accepted despite non-monophyly;
- tuning parameters until communities resemble expected taxonomy;
- orthogroup clustering used to define groups and then presented as independent evidence that groups differ in gene content;
- all genomes force-assigned despite unstable boundaries;
- a fused network treated as more authoritative than the canonical tree;
- average similarity reported without within/between distributions and coverage.
