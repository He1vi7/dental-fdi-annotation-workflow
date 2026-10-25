# -*- coding: utf-8 -*-
"""理想牙弓/槽位差集 + 邻接校验（第一版）。

输入 pred.csv：image, age, fdi, conf, x1,y1,x2,y2
输出 per_image.csv + summary.csv

注意：需要 YOLOv8-FDI 的输出；当前 Tooth_1..32 不能直接用。
"""

import argparse
import os

import pandas as pd

PERM = [11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27, 28,
        31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48]
PRIM = [51, 52, 53, 54, 55, 61, 62, 63, 64, 65,
        71, 72, 73, 74, 75, 81, 82, 83, 84, 85]
# 6-11 岁近似混合模板：乳牙 + 已萌恒切牙/第一磨牙
MIXED = PRIM + [11, 12, 21, 22, 31, 32, 41, 42, 16, 26, 36, 46]


def template(age):
    if age < 6:
        return PRIM
    if age < 12:
        return MIXED
    return PERM


def quadrant(fdi):
    return str(fdi)[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pred", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    d = pd.read_csv(a.pred)
    rows = []
    for img, g in d.groupby("image"):
        age = float(g["age"].iloc[0])
        tpl = template(age)
        det = set(int(x) for x in g["fdi"].dropna().unique())
        missing = [f for f in tpl if f not in det]
        for f in missing:
            q = quadrant(f)
            same_q = [x for x in tpl if quadrant(x) == q]
            idx = same_q.index(f) if f in same_q else -1
            left = same_q[idx - 1] if idx > 0 else None
            right = same_q[idx + 1] if 0 <= idx < len(same_q) - 1 else None
            if left in det and right in det:
                kind = "true_candidate"
            elif left is None or right is None:
                kind = "suspect_miss"
            else:
                kind = "review"
            rows.append({"image": img, "age": age, "missing_fdi": f,
                         "left": left, "right": right, "kind": kind})
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(a.out, "per_image.csv"), index=False, encoding="utf-8-sig")
    summary = out.groupby(["image", "kind"]).size().unstack(fill_value=0).reset_index()
    summary.to_csv(os.path.join(a.out, "summary.csv"), index=False, encoding="utf-8-sig")
    print(out.to_string(index=False) if len(out) else "无缺失候选")


if __name__ == "__main__":
    main()
