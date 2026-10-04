#!/usr/bin/env python3
"""Validate wide pairwise matrices for square shape, labels, symmetry, and missingness.

Use repeated --matrix NAME=PATH arguments. CSV is detected by .csv extension;
all other files are treated as tab-separated.
"""
from __future__ import annotations
import argparse, csv

NA = {"", "NA", "N/A", "NONE", ".", "NULL", "NAN"}

def load(path):
    delim = "," if path.lower().endswith(".csv") else "\t"
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.reader(fh, delimiter=delim))
    if len(rows) < 2 or len(rows[0]) < 2:
        raise ValueError("matrix is empty or malformed")
    cols = rows[0][1:]
    rids, vals = [], []
    for r in rows[1:]:
        if len(r) != len(cols) + 1:
            raise ValueError(f"row has {len(r)} fields; expected {len(cols)+1}")
        rids.append(r[0])
        vals.append(r[1:])
    return cols, rids, vals

def fnum(x):
    if x.strip().upper() in NA:
        return None
    return float(x)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--matrix", action="append", required=True, help="NAME=PATH; repeat")
    ap.add_argument("--symmetry-tol", type=float, default=1e-8)
    ap.add_argument("-o", "--output", required=True)
    args = ap.parse_args()
    records, label_sets = [], {}
    for spec in args.matrix:
        if "=" not in spec:
            raise SystemExit("--matrix must be NAME=PATH")
        name, path = spec.split("=", 1)
        cols, rows, vals = load(path)
        square = len(cols) == len(rows)
        same_order = cols == rows
        label_sets[name] = set(rows)
        missing = 0; numbers = []; asym = 0; compared = 0
        if square and set(cols) == set(rows):
            cidx = {x:i for i,x in enumerate(cols)}
            ridx = {x:i for i,x in enumerate(rows)}
            for a in rows:
                for b in cols:
                    x = fnum(vals[ridx[a]][cidx[b]])
                    if x is None:
                        missing += 1
                    else:
                        numbers.append(x)
                    if a < b and b in ridx and a in cidx:
                        y = fnum(vals[ridx[b]][cidx[a]])
                        if x is not None and y is not None:
                            compared += 1
                            if abs(x-y) > args.symmetry_tol:
                                asym += 1
        records.append([name, path, len(rows), len(cols), square, same_order,
                        len(set(rows)), len(set(cols)), missing,
                        "NA" if not numbers else min(numbers),
                        "NA" if not numbers else max(numbers), compared, asym])
    all_same = len({frozenset(x) for x in label_sets.values()}) == 1
    with open(args.output, "w", newline="", encoding="utf-8") as out:
        w = csv.writer(out, delimiter="\t")
        w.writerow(["matrix", "path", "n_rows", "n_cols", "square", "row_col_same_order",
                    "unique_rows", "unique_cols", "missing_cells", "observed_min", "observed_max",
                    "symmetry_pairs_compared", "asymmetry_failures"])
        w.writerows(records)
        w.writerow(["__ALL_MATRICES_SAME_LABEL_SET__", str(all_same)])
    if not all_same or any(not r[4] for r in records) or any(r[-1] for r in records):
        raise SystemExit(2)

if __name__ == "__main__":
    main()
