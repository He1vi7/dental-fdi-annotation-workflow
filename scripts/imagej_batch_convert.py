# -*- coding: utf-8 -*-
"""批量把 ImageJ Measure CSV 转成统一 FDI 框 CSV。

要求 Measure 文件名：<图名>_measure.csv
图片目录里能找到 <图名>.png / .jpg。
"""

import argparse
import glob
import os
import re

import pandas as pd


def read_any(path):
    last = None
    for enc in ("utf-8-sig", "gbk", "latin1"):
        try:
            return pd.read_csv(path, sep=None, engine="python", encoding=enc)
        except UnicodeDecodeError as e:
            last = e
    raise last


def fdi_of(label):
    s = str(label).split(":")[-1]
    m = re.search(r"\d{1,2}", s)
    return int(m.group(0)) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="*_measure.csv 所在目录")
    ap.add_argument("--images", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    rows = []
    files = sorted(glob.glob(os.path.join(a.dir, "*_measure.csv")))
    if not files:
        raise SystemExit("没找到 *_measure.csv")
    for f in files:
        stem = os.path.basename(f).replace("_measure.csv", "")
        img = None
        for ext in (".png", ".jpg", ".jpeg"):
            p = os.path.join(a.images, stem + ext)
            if os.path.exists(p):
                img = stem + ext
                break
        if not img:
            print("找不到对应图片，跳过:", stem)
            continue
        d = read_any(f)
        for c in ["Label", "Width", "Height"]:
            if c not in d.columns:
                raise SystemExit(f"{f} 缺列 {c}")
        xcol = "X" if "X" in d.columns else "BX"
        ycol = "Y" if "Y" in d.columns else "BY"
        if xcol not in d.columns or ycol not in d.columns:
            raise SystemExit(f"{f} 缺 X/Y 或 BX/BY")
        for _, r in d.iterrows():
            fdi = fdi_of(r["Label"])
            if not fdi:
                continue
            x, y = float(r[xcol]), float(r[ycol])
            w, h = float(r["Width"]), float(r["Height"])
            rows.append([img, fdi, round(x), round(y), round(x + w), round(y + h), "", ""])
    out = pd.DataFrame(rows, columns=["文件名", "FDI", "x1", "y1", "x2", "y2", "presence", "备注"])
    out.to_csv(a.out, index=False, encoding="utf-8-sig")
    print(f"{len(files)} 张图，{len(out)} 个框 -> {a.out}")


if __name__ == "__main__":
    main()
