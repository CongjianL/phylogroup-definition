#!/usr/bin/env python3
"""Check whether each proposed group is exactly monophyletic on a Newick tree.

Requires Biopython. Membership is a TSV with configurable tip and group columns.
"""
from __future__ import annotations
import argparse, csv
try:
    from Bio import Phylo
except ImportError as e:
    raise SystemExit("Biopython is required: install 'biopython'") from e

MISSING = {"", "NA", "N/A", "NONE", ".", "NULL", "UNRESOLVED_PHYLOGROUP"}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", required=True)
    ap.add_argument("--membership", required=True)
    ap.add_argument("--tip-column", default="GenomeID")
    ap.add_argument("--group-column", default="phylogroup")
    ap.add_argument("-o", "--output", required=True)
    args = ap.parse_args()
    tree = Phylo.read(args.tree, "newick")
    terminals = {t.name: t for t in tree.get_terminals()}
    groups = {}
    with open(args.membership, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            gid, grp = r[args.tip_column], r[args.group_column]
            if grp.upper() in MISSING:
                continue
            groups.setdefault(grp, []).append(gid)
    with open(args.output, "w", newline="", encoding="utf-8") as out:
        w = csv.writer(out, delimiter="\t")
        w.writerow(["group", "n_members", "n_missing_from_tree", "missing_tips", "mrca_descendants",
                    "foreign_descendants", "monophyletic"])
        for grp in sorted(groups):
            ids = groups[grp]
            missing = sorted(set(ids) - terminals.keys())
            present = [terminals[x] for x in ids if x in terminals]
            if not present:
                w.writerow([grp, len(ids), len(missing), ";".join(missing), "NA", "NA", False])
                continue
            mrca = tree.common_ancestor(present)
            desc = {t.name for t in mrca.get_terminals()}
            target = set(ids) & terminals.keys()
            foreign = sorted(desc - target)
            mono = not missing and desc == target
            w.writerow([grp, len(ids), len(missing), ";".join(missing), len(desc), len(foreign), mono])

if __name__ == "__main__":
    main()
