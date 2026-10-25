# -*- coding: utf-8 -*-
"""微调 YOLOv8-FDI。"""

import argparse
from ultralytics import YOLO


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--base", default="yolov8n.pt",
                    help="建议先用 yolov8n.pt 建 FDI 头；也可试 best.pt")
    ap.add_argument("--epochs", type=int, default=80)
    ap.add_argument("--imgsz", type=int, default=1280)
    ap.add_argument("--batch", type=int, default=4)
    ap.add_argument(
        "--fliplr",
        type=float,
        default=0.0,
        help="左右翻转概率；FDI 类别含左右象限，默认关闭",
    )
    ap.add_argument("--project", default="runs_fdi")
    ap.add_argument("--name", default="fdi_yolov8n")
    a = ap.parse_args()

    model = YOLO(a.base)
    model.train(data=a.data, epochs=a.epochs, imgsz=a.imgsz, batch=a.batch,
                fliplr=a.fliplr, project=a.project, name=a.name,
                patience=20, workers=4)
    metrics = model.val()
    print(metrics)
    print("best:", model.trainer.best)


if __name__ == "__main__":
    main()
