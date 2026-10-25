# -*- coding: utf-8 -*-
"""把 FDI 框 CSV 转成 YOLO 检测数据集。

CSV 列：文件名,FDI,x1,y1,x2,y2,presence,备注
presence 为空或 1 才写框；2/3/4/5 跳过。
"""

import argparse
import os
import random
import shutil

import pandas as pd
from PIL import Image

FDI = [11, 12, 13, 14, 15, 16, 17, 18,
       21, 22, 23, 24, 25, 26, 27, 28,
       31, 32, 33, 34, 35, 36, 37, 38,
       41, 42, 43, 44, 45, 46, 47, 48,
       51, 52, 53, 54, 55, 61, 62, 63, 64, 65,
       71, 72, 73, 74, 75, 81, 82, 83, 84, 85]
CLS = {f: i for i, f in enumerate(FDI)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", required=True)
    ap.add_argument("--images", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--val-frac", type=float, default=0.2)
    a = ap.parse_args()

    df = pd.read_csv(a.labels)
    if df.empty:
        raise SystemExit("标注模板为空：先标 pilot_50/FDI框_标注模板.csv")
    df = df.dropna(subset=["FDI", "x1", "y1", "x2", "y2"]).copy()
    df["FDI"] = df["FDI"].astype(int)
    df = df[df["FDI"].isin(CLS)]
    pres = df["presence"].astype(str).str.strip()
    df = df[pres.isin(["", "1", "1.0", "nan"]) | df["presence"].isna()]
    if df.empty:
        raise SystemExit("没有可用框：presence 需为空或 1")

    for sub in ("images/train", "images/val", "labels/train", "labels/val"):
        os.makedirs(os.path.join(a.out, sub), exist_ok=True)

    files = sorted(df["文件名"].unique())
    random.seed(42)
    random.shuffle(files)
    nval = max(1, int(round(len(files) * a.val_frac)))
    val = set(files[:nval])

    written = 0
    for fn in files:
        src = os.path.join(a.images, fn)
        if not os.path.exists(src):
            print("缺图，跳过:", src)
            continue
        split = "val" if fn in val else "train"
        shutil.copy2(src, os.path.join(a.out, "images", split, fn))
        W, H = Image.open(src).size
        lines = []
        for _, r in df[df["文件名"] == fn].iterrows():
            x1, y1, x2, y2 = [float(r[k]) for k in ("x1", "y1", "x2", "y2")]
            x1, x2 = max(0, min(x1, x2)), min(W, max(x1, x2))
            y1, y2 = max(0, min(y1, y2)), min(H, max(y1, y2))
            if x2 <= x1 or y2 <= y1:
                continue
            cx, cy = (x1 + x2) / 2 / W, (y1 + y2) / 2 / H
            bw, bh = (x2 - x1) / W, (y2 - y1) / H
            lines.append(f"{CLS[int(r['FDI'])]} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}")
            written += 1
        with open(os.path.join(a.out, "labels", split, os.path.splitext(fn)[0] + ".txt"),
                  "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    with open(os.path.join(a.out, "data.yaml"), "w", encoding="utf-8") as f:
        f.write(f"path: {os.path.abspath(a.out)}\n")
        f.write("train: images/train\nval: images/val\n")
        f.write("names:\n")
        for fdi, i in CLS.items():
            f.write(f"  {i}: '{fdi}'\n")
    print(f"图片 {len(files)} 张，框 {written} 个，train/val 已写入 {a.out}")


if __name__ == "__main__":
    main()
