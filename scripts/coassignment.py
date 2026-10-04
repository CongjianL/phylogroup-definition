#!/usr/bin/env python3
"""Build co-assignment and comparable-count matrices from sweep partitions."""
from __future__ import annotations
import argparse, csv

MISSING = {"", "NA", "N/A", "NONE", ".", "NULL"}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("table", help="TSV: sample ID first, sweep partitions in remaining columns")
    ap.add_argument("--coassignment", required=True)
    ap.add_argument("--counts", required=True)
    args = ap.parse_args()
    with open(args.table, newline="", encoding="utf-8") as fh:
        rows = list(csv.reader(fh, delimiter="\t"))
    if len(rows) < 2 or len(rows[0]) < 2:
        raise SystemExit("Need samples and at least one partition")
    ids = [r[0] for r in rows[1:]]
    labels = [r[1:] for r in rows[1:]]
    n = len(ids)
    num = [[0] * n for _ in range(n)]
    den = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            for a, b in zip(labels[i], labels[j]):
                if a.upper() in MISSING or b.upper() in MISSING:
                    continue
                den[i][j] += 1
                den[j][i] += 1 if j != i else 0
                if a == b:
                    num[i][j] += 1
                    num[j][i] += 1 if j != i else 0
    def write(path, values, fraction=False):
        with open(path, "w", newline="", encoding="utf-8") as out:
            w = csv.writer(out, delimiter="\t")
            w.writerow(["GenomeID", *ids])
            for i, gid in enumerate(ids):
                row = []
                for j in range(n):
                    if fraction:
                        row.append("NA" if den[i][j] == 0 else f"{num[i][j]/den[i][j]:.10g}")
                    else:
                        row.append(str(values[i][j]))
                w.writerow([gid, *row])
    write(args.coassignment, num, fraction=True)
    write(args.counts, den, fraction=False)

if __name__ == "__main__":
    main()
