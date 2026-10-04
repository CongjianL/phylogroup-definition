#!/usr/bin/env python3
"""Compare categorical partitions with ARI, NMI, and VI.

Input: TSV with sample ID in the first column and one or more partition columns.
Missing labels (empty, NA, N/A, NONE, .) are excluded pairwise.
NMI uses the arithmetic-mean entropy normalization: 2*MI/(H1+H2).
VI is reported in bits.
"""
from __future__ import annotations
import argparse, csv, math
from collections import Counter

MISSING = {"", "NA", "N/A", "NONE", ".", "NULL"}

def comb2(n: int) -> float:
    return n * (n - 1) / 2.0

def entropy(counts: Counter, n: int) -> float:
    if n == 0:
        return float("nan")
    h = 0.0
    for c in counts.values():
        if c:
            p = c / n
            h -= p * math.log2(p)
    return h

def metrics(a, b):
    pairs = [(x, y) for x, y in zip(a, b) if str(x).upper() not in MISSING and str(y).upper() not in MISSING]
    n = len(pairs)
    if n == 0:
        return n, float("nan"), float("nan"), float("nan")
    ca = Counter(x for x, _ in pairs)
    cb = Counter(y for _, y in pairs)
    joint = Counter(pairs)
    sum_joint = sum(comb2(v) for v in joint.values())
    sum_a = sum(comb2(v) for v in ca.values())
    sum_b = sum(comb2(v) for v in cb.values())
    total = comb2(n)
    if total == 0:
        ari = 1.0 if list(ca.values()) == [1] and list(cb.values()) == [1] else float("nan")
    else:
        expected = (sum_a * sum_b) / total
        max_index = 0.5 * (sum_a + sum_b)
        denom = max_index - expected
        ari = (sum_joint - expected) / denom if denom else 1.0
    ha, hb = entropy(ca, n), entropy(cb, n)
    mi = 0.0
    for (x, y), c in joint.items():
        pxy = c / n
        px = ca[x] / n
        py = cb[y] / n
        mi += pxy * math.log2(pxy / (px * py))
    nmi = 1.0 if ha + hb == 0 else 2.0 * mi / (ha + hb)
    vi = ha + hb - 2.0 * mi
    if abs(vi) < 1e-12:
        vi = 0.0
    return n, ari, nmi, vi

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("table", help="TSV: first column sample ID, remaining columns partitions")
    ap.add_argument("-o", "--output", required=True)
    args = ap.parse_args()
    with open(args.table, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    if not rows:
        raise SystemExit("No rows found")
    fields = list(rows[0])
    if len(fields) < 3:
        raise SystemExit("Need sample ID plus at least two partition columns")
    parts = fields[1:]
    with open(args.output, "w", newline="", encoding="utf-8") as out:
        w = csv.writer(out, delimiter="\t")
        w.writerow(["partition_a", "partition_b", "n_comparable", "ARI", "NMI", "VI_bits"])
        for i in range(len(parts)):
            for j in range(i + 1, len(parts)):
                p, q = parts[i], parts[j]
                n, ari, nmi, vi = metrics([r[p] for r in rows], [r[q] for r in rows])
                w.writerow([p, q, n, f"{ari:.10g}", f"{nmi:.10g}", f"{vi:.10g}"])

if __name__ == "__main__":
    main()
